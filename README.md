package co.com.bnpparibas.cardif.closingclaims.domain.services.impl;

import java.time.LocalDateTime;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Optional;

import co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcardif.ClosingCardif;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia.ColombiaAccountingLine;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia.ColombiaAccountingResultDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia.ColombiaXmlFile;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia.ColombiaXmlFileDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.entity.ArchivoAsientoCardif;
import co.com.bnpparibas.cardif.closingclaims.domain.entity.ArchivoAsientoCardifXml;
import co.com.bnpparibas.cardif.closingclaims.domain.util.exception.BusinessException;
import co.com.bnpparibas.cardif.closingclaims.domain.util.helpers.ColombiaAccountingXmlHelper;
import co.com.bnpparibas.cardif.closingclaims.infraestructure.repository.ArchivoAsientoCardifXmlRepository;
import co.com.bnpparibas.cardif.closingclaims.infraestructure.repository.ClosingCardifRepository;
import co.com.bnpparibas.cardif.closingclaims.infraestructure.repository.StoredProcedureExecutor;
import co.com.bnpparibas.cardif.closingclaims.infraestructure.repository.StoredProcedureRowMapper;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.dao.DataAccessResourceFailureException;
import org.springframework.http.HttpStatus;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyList;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
public class ClosingCardifServiceImplTest {

    private static final String P_HEADER = "hdr";
    private static final String CORRELATION_ID = "corr-123";
    private static final String REQUEST_ID = "req-456";

    @Mock
    private ClosingCardifRepository closingCardifRepository;

    @Mock
    private ArchivoAsientoCardifXmlRepository fileRepository;

    @Mock
    private ColombiaAccountingXmlHelper xmlHelper;

    @Mock
    private StoredProcedureExecutor storedProcedureExecutor;

    @InjectMocks
    private ClosingCardifServiceImpl service;

    private ColombiaAccountingLine line() {
        return ColombiaAccountingLine.builder()
                .family("ReasegCardif")
                .period("202608")
                .pass(1)
                .movementType("Pago")
                .sequence(1L)
                .content("<Line/>")
                .build();
    }

    private ColombiaXmlFile file() {
        return ColombiaXmlFile.builder()
                .family("ReasegCardif")
                .period("202608")
                .movementType("Pago")
                .fileName("ReasegDirectasPago20260827.xml")
                .lineCount(1)
                .content("<SSC/>")
                .build();
    }

    private ArchivoAsientoCardifXml entity() {
        return ArchivoAsientoCardifXml.builder()
                .id(1)
                .idLote("lote")
                .periodo("202608")
                .familia("ReasegCardif")
                .tipoMovimiento("Pago")
                .nombreArchivo("ReasegDirectasPago20260827.xml")
                .contenido("<SSC/>")
                .cantidadLineas(1)
                .fechaproceso(LocalDateTime.of(2026, 8, 27, 15, 3, 29))
                .estado("GENERADO")
                .build();
    }

    @Nested
    @DisplayName("getDetailsReportsCardif")
    class GetDetailsReportsCardif {

        @Test
        @DisplayName("debe devolver lista mapeada cuando el repositorio retorna datos")
        void shouldReturnMappedList() {
            ArchivoAsientoCardif entity = new ArchivoAsientoCardif();
            entity.setNombreArchivo("archivo1.txt");
            entity.setFechaproceso(LocalDateTime.of(2024, 5, 1, 10, 30));
            entity.setEstado("PROCESADO");

            when(closingCardifRepository.findAllDetailsCardif())
                    .thenReturn(Arrays.asList(entity));

            List<ClosingCardif> result = service.getDetailsReportsCardif("hdr", "corrId", "reqId");

            assertNotNull(result);
            assertEquals(1, result.size());

            ClosingCardif dto = result.get(0);
            assertEquals("archivo1.txt", dto.getNombreArchivo());
            assertEquals(LocalDateTime.of(2024, 5, 1, 10, 30), dto.getDateProcessing());
            assertEquals("PROCESADO", dto.getStatus());

            verify(closingCardifRepository, times(1)).findAllDetailsCardif();
        }

        @Test
        @DisplayName("debe lanzar BusinessException cuando no hay registros")
        void shouldThrowExceptionWhenNoData() {
            when(closingCardifRepository.findAllDetailsCardif())
                    .thenReturn(Collections.emptyList());

            BusinessException ex = assertThrows(
                    BusinessException.class,
                    () -> service.getDetailsReportsCardif("hdr", "corrId", "reqId")
            );

            assertEquals("No registros para consultar", ex.getMessage());
            assertEquals(HttpStatus.BAD_REQUEST, ex.getHttpStatus());

            verify(closingCardifRepository, times(1)).findAllDetailsCardif();
        }
    }

    @Test
    @DisplayName("debe lanzar BusinessException cuando el repositorio devuelve null")
    void shouldThrowExceptionWhenRepositoryReturnsNull() {
        when(closingCardifRepository.findAllDetailsCardif())
                .thenReturn(null);

        BusinessException ex = assertThrows(
                BusinessException.class,
                () -> service.getDetailsReportsCardif("hdr", "corrId", "reqId")
        );

        assertEquals("No registros para consultar", ex.getMessage());
        assertEquals(HttpStatus.BAD_REQUEST, ex.getHttpStatus());

        verify(closingCardifRepository, times(1)).findAllDetailsCardif();
    }


    @Nested
    @DisplayName("uploadReportsPendingRptCardif")
    class UploadReportsPendingRptCardif {

        @Test
        @DisplayName("debe devolver mensaje con filas afectadas cuando la actualización es exitosa")
        void shouldReturnSuccessMessage() {
            when(closingCardifRepository.markAsPendingRptCardif()).thenReturn(5);

            String result = service.uploadReportsPendingRptCardif("hdr", "corrId", "reqId");

            assertEquals("Actualización completada, filas afectadas: 5", result);
            verify(closingCardifRepository, times(1)).markAsPendingRptCardif();
        }

        @Test
        @DisplayName("debe devolver mensaje de error cuando el repositorio lanza excepción")
        void shouldReturnErrorMessageOnException() {
            when(closingCardifRepository.markAsPendingRptCardif())
                    .thenThrow(new RuntimeException("Fallo DB"));

            BusinessException ex = assertThrows(
                    BusinessException.class,
                    () -> service.uploadReportsPendingRptCardif("hdr", "corrId", "reqId")
            );

            assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, ex.getHttpStatus());
            assertEquals("Error al actualizar reporte", ex.getMessage());
            assertEquals("Fallo DB", ex.getCause().getMessage());

            verify(closingCardifRepository, times(1)).markAsPendingRptCardif();
        }
    }

    @Nested
    @DisplayName("generateAccountingEntries")
    class GenerateAccountingEntries {

        @Test
        @DisplayName("debe persistir los archivos generados y devolverlos")
        void shouldPersistGeneratedFiles() {
            when(closingCardifRepository.countAvalClosingControl())
                    .thenReturn(1);
            when(storedProcedureExecutor.query(
                    anyString(),
                    any(StoredProcedureRowMapper.class),
                    anyString()))
                    .thenReturn(Collections.singletonList(line()));
            when(xmlHelper.buildFiles(anyList()))
                    .thenReturn(Collections.singletonList(file()));
            when(fileRepository.saveAll(anyList()))
                    .thenReturn(Collections.singletonList(entity()));

            ColombiaAccountingResultDTO result =
                    service.generateAccountingEntries(
                            P_HEADER, CORRELATION_ID, REQUEST_ID);

            assertEquals("Asientos generados con éxito.", result.getMessage());
            assertEquals("202608", result.getPeriod());
            assertEquals(1, result.getFiles().size());
            assertEquals("ReasegCardif", result.getFiles().get(0).getFamily());
            assertEquals("GENERADO", result.getFiles().get(0).getStatus());

            verify(fileRepository, times(1)).deleteAllFiles();
            verify(storedProcedureExecutor, times(2)).query(
                    anyString(),
                    any(StoredProcedureRowMapper.class),
                    anyString());
        }

        @Test
        @DisplayName("debe lanzar BusinessException cuando el cierre de aval no se ejecuto")
        void shouldThrowWhenAvalClosingIsMissing() {
            when(closingCardifRepository.countAvalClosingControl())
                    .thenReturn(0);

            BusinessException ex = assertThrows(
                    BusinessException.class,
                    () -> service.generateAccountingEntries(
                            P_HEADER, CORRELATION_ID, REQUEST_ID));

            assertEquals(HttpStatus.BAD_REQUEST, ex.getHttpStatus());
            assertEquals(
                    "Debe ejecutar primero el cierre de Aval",
                    ex.getMessage());

            verify(fileRepository, never()).deleteAllFiles();
        }

        @Test
        @DisplayName("debe lanzar BusinessException cuando no se generan archivos")
        void shouldThrowWhenNoFilesGenerated() {
            when(closingCardifRepository.countAvalClosingControl())
                    .thenReturn(1);
            when(storedProcedureExecutor.query(
                    anyString(),
                    any(StoredProcedureRowMapper.class),
                    anyString()))
                    .thenReturn(Collections.emptyList());
            when(xmlHelper.buildFiles(anyList()))
                    .thenReturn(Collections.emptyList());

            BusinessException ex = assertThrows(
                    BusinessException.class,
                    () -> service.generateAccountingEntries(
                            P_HEADER, CORRELATION_ID, REQUEST_ID));

            assertEquals(HttpStatus.NOT_FOUND, ex.getHttpStatus());
            assertEquals(
                    "No se generaron asientos contables para el periodo",
                    ex.getMessage());
        }

        @Test
        @DisplayName("debe lanzar BusinessException cuando el helper falla")
        void shouldThrowWhenHelperFails() {
            when(closingCardifRepository.countAvalClosingControl())
                    .thenReturn(1);
            when(storedProcedureExecutor.query(
                    anyString(),
                    any(StoredProcedureRowMapper.class),
                    anyString()))
                    .thenReturn(Collections.singletonList(line()));
            when(xmlHelper.buildFiles(anyList()))
                    .thenThrow(new IllegalStateException("boom"));

            BusinessException ex = assertThrows(
                    BusinessException.class,
                    () -> service.generateAccountingEntries(
                            P_HEADER, CORRELATION_ID, REQUEST_ID));

            assertEquals(
                    HttpStatus.INTERNAL_SERVER_ERROR, ex.getHttpStatus());
            assertEquals(
                    "Error al generar los archivos XML contables",
                    ex.getMessage());
        }

        @Test
        @DisplayName("debe lanzar BusinessException cuando falla el acceso a datos")
        void shouldThrowWhenDatabaseFails() {
            when(closingCardifRepository.countAvalClosingControl())
                    .thenThrow(new DataAccessResourceFailureException("db"));

            BusinessException ex = assertThrows(
                    BusinessException.class,
                    () -> service.generateAccountingEntries(
                            P_HEADER, CORRELATION_ID, REQUEST_ID));

            assertEquals(
                    HttpStatus.INTERNAL_SERVER_ERROR, ex.getHttpStatus());
            assertEquals(
                    "Error al acceder a la informacion del cierre de movimientos",
                    ex.getMessage());
        }

        @Test
        @DisplayName("debe lanzar BusinessException cuando falla el borrado previo")
        void shouldThrowWhenDeleteFails() {
            when(closingCardifRepository.countAvalClosingControl())
                    .thenReturn(1);
            when(fileRepository.deleteAllFiles())
                    .thenThrow(new DataAccessResourceFailureException("db"));

            BusinessException ex = assertThrows(
                    BusinessException.class,
                    () -> service.generateAccountingEntries(
                            P_HEADER, CORRELATION_ID, REQUEST_ID));

            assertEquals(
                    HttpStatus.INTERNAL_SERVER_ERROR, ex.getHttpStatus());
        }

        @Test
        @DisplayName("debe lanzar BusinessException cuando falla el guardado")
        void shouldThrowWhenSaveFails() {
            when(closingCardifRepository.countAvalClosingControl())
                    .thenReturn(1);
            when(storedProcedureExecutor.query(
                    anyString(),
                    any(StoredProcedureRowMapper.class),
                    anyString()))
                    .thenReturn(Collections.singletonList(line()));
            when(xmlHelper.buildFiles(anyList()))
                    .thenReturn(Collections.singletonList(file()));
            when(fileRepository.saveAll(anyList()))
                    .thenThrow(new DataAccessResourceFailureException("db"));

            BusinessException ex = assertThrows(
                    BusinessException.class,
                    () -> service.generateAccountingEntries(
                            P_HEADER, CORRELATION_ID, REQUEST_ID));

            assertEquals(
                    HttpStatus.INTERNAL_SERVER_ERROR, ex.getHttpStatus());
        }

        @Test
        @DisplayName("debe lanzar BusinessException cuando falla el procedimiento")
        void shouldThrowWhenProcedureFails() {
            when(closingCardifRepository.countAvalClosingControl())
                    .thenReturn(1);
            when(storedProcedureExecutor.query(
                    anyString(),
                    any(StoredProcedureRowMapper.class),
                    anyString()))
                    .thenThrow(new DataAccessResourceFailureException("db"));

            BusinessException ex = assertThrows(
                    BusinessException.class,
                    () -> service.generateAccountingEntries(
                            P_HEADER, CORRELATION_ID, REQUEST_ID));

            assertEquals(
                    HttpStatus.INTERNAL_SERVER_ERROR, ex.getHttpStatus());
        }
    }

    @Nested
    @DisplayName("findGeneratedFiles")
    class FindGeneratedFiles {

        @Test
        @DisplayName("debe devolver los archivos persistidos")
        void shouldReturnPersistedFiles() {
            when(fileRepository.findLatest())
                    .thenReturn(Collections.singletonList(entity()));

            List<ColombiaXmlFileDTO> files =
                    service.findGeneratedFiles(CORRELATION_ID, REQUEST_ID);

            assertEquals(1, files.size());
            assertEquals(1, files.get(0).getId());
            assertEquals("ReasegCardif", files.get(0).getFamily());
            assertNotNull(files.get(0).getProcessDate());
        }

        @Test
        @DisplayName("debe devolver fecha nula cuando la entidad no la tiene")
        void shouldReturnNullProcessDate() {
            ArchivoAsientoCardifXml withoutDate = entity();
            withoutDate.setFechaproceso(null);

            when(fileRepository.findLatest())
                    .thenReturn(Collections.singletonList(withoutDate));

            List<ColombiaXmlFileDTO> files =
                    service.findGeneratedFiles(CORRELATION_ID, REQUEST_ID);

            assertNull(files.get(0).getProcessDate());
        }

        @Test
        @DisplayName("debe lanzar BusinessException cuando falla la consulta")
        void shouldThrowWhenQueryFails() {
            when(fileRepository.findLatest())
                    .thenThrow(new DataAccessResourceFailureException("db"));

            BusinessException ex = assertThrows(
                    BusinessException.class,
                    () -> service.findGeneratedFiles(
                            CORRELATION_ID, REQUEST_ID));

            assertEquals(
                    HttpStatus.INTERNAL_SERVER_ERROR, ex.getHttpStatus());
        }
    }

    @Nested
    @DisplayName("findXmlFile")
    class FindXmlFile {

        @Test
        @DisplayName("debe devolver el archivo solicitado")
        void shouldReturnRequestedFile() {
            when(fileRepository.findById(1))
                    .thenReturn(Optional.of(entity()));

            ArchivoAsientoCardifXml file =
                    service.findXmlFile(1, CORRELATION_ID, REQUEST_ID);

            assertEquals(1, file.getId());
            assertEquals("<SSC/>", file.getContenido());
        }

        @Test
        @DisplayName("debe lanzar BusinessException cuando el archivo no existe")
        void shouldThrowWhenFileIsMissing() {
            when(fileRepository.findById(9))
                    .thenReturn(Optional.empty());

            BusinessException ex = assertThrows(
                    BusinessException.class,
                    () -> service.findXmlFile(
                            9, CORRELATION_ID, REQUEST_ID));

            assertEquals(HttpStatus.NOT_FOUND, ex.getHttpStatus());
            assertEquals(
                    "El archivo XML solicitado no existe", ex.getMessage());
        }

        @Test
        @DisplayName("debe lanzar BusinessException cuando el archivo no tiene contenido")
        void shouldThrowWhenContentIsMissing() {
            ArchivoAsientoCardifXml withoutContent = entity();
            withoutContent.setContenido(null);

            when(fileRepository.findById(1))
                    .thenReturn(Optional.of(withoutContent));

            BusinessException ex = assertThrows(
                    BusinessException.class,
                    () -> service.findXmlFile(
                            1, CORRELATION_ID, REQUEST_ID));

            assertEquals(HttpStatus.NOT_FOUND, ex.getHttpStatus());
        }

        @Test
        @DisplayName("debe lanzar BusinessException cuando falla la consulta")
        void shouldThrowWhenQueryFails() {
            when(fileRepository.findById(1))
                    .thenThrow(new DataAccessResourceFailureException("db"));

            BusinessException ex = assertThrows(
                    BusinessException.class,
                    () -> service.findXmlFile(
                            1, CORRELATION_ID, REQUEST_ID));

            assertEquals(
                    HttpStatus.INTERNAL_SERVER_ERROR, ex.getHttpStatus());
        }
    }
}
