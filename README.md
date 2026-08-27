package co.com.bnpparibas.cardif.closingclaims.domain.services.impl;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyList;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.*;

import java.time.LocalDateTime;
import java.util.Collections;
import java.util.List;
import java.util.Optional;

import co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia.ColombiaAccountingLine;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia.ColombiaAccountingResultDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia.ColombiaXmlFile;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia.ColombiaXmlFileDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.entity.ArchivoAsientoAvalXml;
import co.com.bnpparibas.cardif.closingclaims.domain.util.helpers.ColombiaAccountingXmlHelper;
import co.com.bnpparibas.cardif.closingclaims.infraestructure.repository.ArchivoAsientoAvalXmlRepository;
import co.com.bnpparibas.cardif.closingclaims.infraestructure.repository.ClosingAvalRepository;
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
import co.com.bnpparibas.cardif.closingclaims.domain.util.exception.BusinessException;

import co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingaval.ClosingAval;
import co.com.bnpparibas.cardif.closingclaims.domain.entity.TmpRepAvalCierre;


@ExtendWith(MockitoExtension.class)
public class ClosingAvalServiceImplTest {

    private static final String P_HEADER = "hdr";
    private static final String CORRELATION_ID = "corr-123";
    private static final String REQUEST_ID = "req-456";

    @Mock
    private ClosingAvalRepository closingAvalRepository;

    @Mock
    private ArchivoAsientoAvalXmlRepository fileRepository;

    @Mock
    private ColombiaAccountingXmlHelper xmlHelper;

    @Mock
    private StoredProcedureExecutor storedProcedureExecutor;

    @InjectMocks
    private ClosingAvalServiceImpl service;

    private ColombiaAccountingLine line() {
        return ColombiaAccountingLine.builder()
                .family("ReasegAlfa")
                .period("202608")
                .pass(1)
                .movementType("Constitucion")
                .sequence(1L)
                .content("<Line/>")
                .build();
    }

    private ColombiaXmlFile file() {
        return ColombiaXmlFile.builder()
                .family("ReasegAlfa")
                .period("202608")
                .movementType("Constitucion")
                .fileName("ReasegAlf_HogarConstitucion20260827.xml")
                .lineCount(1)
                .content("<SSC/>")
                .build();
    }

    private ArchivoAsientoAvalXml entity() {
        return ArchivoAsientoAvalXml.builder()
                .id(1)
                .idLote("lote")
                .periodo("202608")
                .familia("ReasegAlfa")
                .tipoMovimiento("Constitucion")
                .nombreArchivo("ReasegAlf_HogarConstitucion20260827.xml")
                .contenido("<SSC/>")
                .cantidadLineas(1)
                .fechaproceso(LocalDateTime.of(2026, 8, 27, 15, 3, 29))
                .estado("GENERADO")
                .build();
    }

    @Test
    @DisplayName("getDetailsReportsAval devuelve lista completa de ClosingAval")
    void getDetailsReportsAval_success() {
        TmpRepAvalCierre detail = new TmpRepAvalCierre();
        LocalDateTime now = LocalDateTime.now();
        detail.setFechagenera(now);
        detail.setEstado("APPROVED");
        detail.setNombreRpt("Rpt001");

        when(closingAvalRepository.findAllDetailsAval())
                .thenReturn(Collections.singletonList(detail));

        List<ClosingAval> result = service.getDetailsReportsAval("hdr", "corrId", "reqId");

        assertNotNull(result);
        assertEquals(1, result.size());

        ClosingAval av = result.get(0);
        assertEquals(now, av.getDateGenerate());
        assertEquals("APPROVED", av.getStatus());
        assertEquals("Rpt001", av.getNombreRpt());

        verify(closingAvalRepository, times(1)).findAllDetailsAval();
    }

    @Test
    @DisplayName("getDetailsReportsAval lanza BusinessException cuando la lista está vacía")
    void getDetailsReportsAval_noData_throwsException() {
        when(closingAvalRepository.findAllDetailsAval())
                .thenReturn(null);

        BusinessException ex = assertThrows(
                BusinessException.class,
                () -> service.getDetailsReportsAval("hdr", "corrId", "reqId")
        );

        assertEquals(HttpStatus.BAD_REQUEST, ex.getHttpStatus());
        assertEquals("No registros para consultar", ex.getMessage());
        verify(closingAvalRepository, times(1)).findAllDetailsAval();
    }

    @Test
    @DisplayName("lanza BusinessException cuando la lista está vacía")
    void getDetailsReportsAval_emptyList_throwsException() {
        when(closingAvalRepository.findAllDetailsAval())
                .thenReturn(Collections.emptyList());

        BusinessException ex = assertThrows(
                BusinessException.class,
                () -> service.getDetailsReportsAval("hdr", "corrId", "reqId"));

        assertEquals(HttpStatus.BAD_REQUEST, ex.getHttpStatus());
        assertEquals("No registros para consultar", ex.getMessage());

        verify(closingAvalRepository, times(1)).findAllDetailsAval();
    }

    @Test
    @DisplayName("uploadReportsPendingRptAval devuelve mensaje con filas actualizadas")
    void uploadReportsPendingRptAval_success() {
        when(closingAvalRepository.markAsPendingRptAval()).thenReturn(5);

        String result = service.uploadReportsPendingRptAval("hdr", "corrId", "reqId");

        assertEquals("Actualización completada, filas afectadas: 5", result);
        verify(closingAvalRepository, times(1)).markAsPendingRptAval();
    }

    @Test
    @DisplayName("cuando el repositorio lanza excepción, se devuelve mensaje de error")
    void uploadReportsPendingRptAval_repositoryThrows() {
        when(closingAvalRepository.markAsPendingRptAval())
                .thenThrow(new RuntimeException("DB error"));

        BusinessException ex = assertThrows(
                BusinessException.class,
                () -> service.uploadReportsPendingRptAval("hdr", "corrId", "reqId")
        );

        assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, ex.getHttpStatus());
        assertEquals("Error al actualizar reporte", ex.getMessage());
        assertEquals("DB error", ex.getCause().getMessage());

        verify(closingAvalRepository, times(1)).markAsPendingRptAval();
    }

    @Test
    @DisplayName("uploadReportsPendingRptAval maneja caso 0 filas actualizadas")
    void uploadReportsPendingRptAval_zeroRows() {
        when(closingAvalRepository.markAsPendingRptAval()).thenReturn(0);

        String result = service.uploadReportsPendingRptAval("hdr", "corrId", "reqId");

        assertEquals("Actualización completada, filas afectadas: 0", result);
        verify(closingAvalRepository, times(1)).markAsPendingRptAval();
    }

    @Test
    @DisplayName("lanza BusinessException cuando el repositorio devuelve null")
    void getReportsSeatAval_null_throwsException() {
        when(closingAvalRepository.findAllReportsAsientoAval())
                .thenReturn(null);

        BusinessException ex = assertThrows(
                BusinessException.class,
                () -> service.getReportsSeatAval("hdr", "corrId", "reqId"));

        assertEquals(HttpStatus.BAD_REQUEST, ex.getHttpStatus());
        assertEquals("No registros para consultar", ex.getMessage());

        verify(closingAvalRepository, times(1)).findAllReportsAsientoAval();
    }

    @Test
    @DisplayName("getReportsSeatAval devuelve lista completa de ClosingAval")
    void getReportsSeatAval_success() {
        ClosingAvalRepository.ArchivoAsientoAvalProjection mockRow =
                mock(ClosingAvalRepository.ArchivoAsientoAvalProjection.class);
        LocalDateTime now = LocalDateTime.now();
        when(mockRow.getFechaproceso()).thenReturn(now);
        when(mockRow.getEstado()).thenReturn("PENDING");
        when(mockRow.getNombreArchivo()).thenReturn("SeatRpt001");

        when(closingAvalRepository.findAllReportsAsientoAval())
                .thenReturn(Collections.singletonList(mockRow));

        List<ClosingAval> result = service.getReportsSeatAval("hdr", "corrId", "reqId");

        assertNotNull(result);
        assertEquals(1, result.size());

        ClosingAval av = result.get(0);
        assertEquals(now, av.getDateGenerate());
        assertEquals("PENDING", av.getStatus());
        assertEquals("SeatRpt001", av.getNombreRpt());

        verify(closingAvalRepository, times(1)).findAllReportsAsientoAval();
    }

    @Test
    @DisplayName("getReportsSeatAval lanza BusinessException cuando no hay registros")
    void getReportsSeatAval_noData_throwsException() {
        when(closingAvalRepository.findAllReportsAsientoAval())
                .thenReturn(Collections.emptyList());

        BusinessException ex = assertThrows(
                BusinessException.class,
                () -> service.getReportsSeatAval("hdr", "corrId", "reqId")
        );

        assertEquals(HttpStatus.BAD_REQUEST, ex.getHttpStatus());
        assertEquals("No registros para consultar", ex.getMessage());

        verify(closingAvalRepository, times(1)).findAllReportsAsientoAval();
    }

    @Test
    @DisplayName("uploadReportsPendingRptSeatAval devuelve mensaje con filas actualizadas")
    void uploadReportsPendingRptSeatAval_success() {
        when(closingAvalRepository.markAsPendingRptSeatAval()).thenReturn(7);

        String result = service.uploadReportsPendingRptSeatAval("hdr", "corrId", "reqId");

        assertEquals("Actualización completada, filas afectadas: 7", result);
        verify(closingAvalRepository, times(1)).markAsPendingRptSeatAval();
    }

    @Test
    @DisplayName("uploadReportsPendingRptSeatAval maneja excepción del repositorio")
    void uploadReportsPendingRptSeatAval_exception() {
        when(closingAvalRepository.markAsPendingRptSeatAval())
                .thenThrow(new RuntimeException("DB error"));

        BusinessException ex = assertThrows(
                BusinessException.class,
                () -> service.uploadReportsPendingRptSeatAval("hdr", "corrId", "reqId")
        );

        assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, ex.getHttpStatus());
        assertEquals("Error al actualizar reporte", ex.getMessage());
        assertEquals("DB error", ex.getCause().getMessage());

        verify(closingAvalRepository, times(1)).markAsPendingRptSeatAval();
    }

    @Nested
    @DisplayName("generateAccountingEntries")
    class GenerateAccountingEntries {

        @Test
        @DisplayName("debe persistir los archivos generados y devolverlos")
        void shouldPersistGeneratedFiles() {
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
            assertEquals("ReasegAlfa", result.getFiles().get(0).getFamily());

            verify(fileRepository, times(1)).deleteAllFiles();
            verify(storedProcedureExecutor, times(1)).query(
                    anyString(),
                    any(StoredProcedureRowMapper.class),
                    anyString());
        }

        @Test
        @DisplayName("debe lanzar BusinessException cuando no se generan archivos")
        void shouldThrowWhenNoFilesGenerated() {
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
        @DisplayName("debe lanzar BusinessException cuando falla el borrado previo")
        void shouldThrowWhenDeleteFails() {
            when(fileRepository.deleteAllFiles())
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
        @DisplayName("debe lanzar BusinessException cuando falla el procedimiento")
        void shouldThrowWhenProcedureFails() {
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

        @Test
        @DisplayName("debe lanzar BusinessException cuando falla el guardado")
        void shouldThrowWhenSaveFails() {
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
            assertEquals("ReasegAlfa", files.get(0).getFamily());
            assertNotNull(files.get(0).getProcessDate());
        }

        @Test
        @DisplayName("debe devolver fecha nula cuando la entidad no la tiene")
        void shouldReturnNullProcessDate() {
            ArchivoAsientoAvalXml withoutDate = entity();
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

            ArchivoAsientoAvalXml file =
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
            ArchivoAsientoAvalXml withoutContent = entity();
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
