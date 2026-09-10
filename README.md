package co.com.bnpparibas.cardif.closingclaims.domain.services.impl;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyList;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.*;
import static org.mockito.Mockito.mock;
import org.mockito.ArgumentCaptor;

import java.time.LocalDateTime;
import java.util.Collections;
import java.util.List;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.io.IOException;
import java.util.Optional;

import co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia.ColombiaAccountingLine;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia.ColombiaAccountingResultDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia.ColombiaXmlFile;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia.ColombiaXmlFileDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.entity.ArchivoAsientoAvalXml;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia.AvalReportRow;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia.AvalReportFileDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.entity.ArchivoReporteAvalExcel;
import co.com.bnpparibas.cardif.closingclaims.domain.util.helpers.AvalReportExcelHelper;
import co.com.bnpparibas.cardif.closingclaims.infraestructure.repository.ArchivoReporteAvalExcelRepository;
import co.com.bnpparibas.cardif.closingclaims.infraestructure.repository.AvalReportRepository;
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
    private AvalReportRepository reportRepository;

    @Mock
    private ArchivoReporteAvalExcelRepository reportFileRepository;

    @Mock
    private AvalReportExcelHelper excelHelper;

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

    @Nested
    @DisplayName("Reporte mensual de Aval")
    class AvalReport {

        private AvalReportRow reportRow() {
            return AvalReportRow.builder()
                    .compania("02")
                    .siniestroLider("0902026A193877")
                    .nombreasegurado("JUAN PEREZ")
                    .build();
        }

        private ArchivoReporteAvalExcel reportFile() {
            return ArchivoReporteAvalExcel.builder()
                    .id(1)
                    .idLote("lote")
                    .periodo("202609")
                    .nombreArchivo("RPT_CIERRE_AVAL.xlsx")
                    .contenido(new byte[] {0x50, 0x4B, 0x03, 0x04})
                    .cantidadFilas(257)
                    .fechaproceso(LocalDateTime.of(2026, 9, 9, 10, 0, 0))
                    .estado("GENERADO")
                    .build();
        }

        @Test
        @DisplayName("findReportStatus devuelve el archivo y los pendientes")
        void shouldReturnFileAndPendingCount() {
            when(reportRepository.countPendingMovements()).thenReturn(93);
            when(reportFileRepository.findLatest())
                    .thenReturn(Collections.singletonList(reportFile()));

            AvalReportFileDTO status =
                    service.findReportStatus(CORRELATION_ID, REQUEST_ID);

            assertEquals(1, status.getId());
            assertEquals("202609", status.getPeriod());
            assertEquals("RPT_CIERRE_AVAL.xlsx", status.getFileName());
            assertEquals(257, status.getRowCount());
            assertEquals("GENERADO", status.getStatus());
            assertEquals(93, status.getPendingMovements());
            assertNotNull(status.getProcessDate());
        }

        @Test
        @DisplayName("findReportStatus devuelve solo pendientes sin archivo")
        void shouldReturnOnlyPendingWhenThereIsNoFile() {
            when(reportRepository.countPendingMovements()).thenReturn(5);
            when(reportFileRepository.findLatest())
                    .thenReturn(Collections.emptyList());

            AvalReportFileDTO status =
                    service.findReportStatus(CORRELATION_ID, REQUEST_ID);

            assertNull(status.getId());
            assertNull(status.getFileName());
            assertEquals(5, status.getPendingMovements());
        }

        @Test
        @DisplayName("findReportStatus devuelve fecha nula cuando falta")
        void shouldReturnNullProcessDate() {
            ArchivoReporteAvalExcel withoutDate = reportFile();
            withoutDate.setFechaproceso(null);

            when(reportRepository.countPendingMovements()).thenReturn(0);
            when(reportFileRepository.findLatest())
                    .thenReturn(Collections.singletonList(withoutDate));

            AvalReportFileDTO status =
                    service.findReportStatus(CORRELATION_ID, REQUEST_ID);

            assertNull(status.getProcessDate());
            assertEquals(0, status.getPendingMovements());
        }

        @Test
        @DisplayName("findReportStatus lanza excepcion si falla el conteo")
        void shouldThrowWhenCountFails() {
            when(reportRepository.countPendingMovements())
                    .thenThrow(new DataAccessResourceFailureException("db"));

            BusinessException ex = assertThrows(
                    BusinessException.class,
                    () -> service.findReportStatus(
                            CORRELATION_ID, REQUEST_ID));

            assertEquals(
                    HttpStatus.INTERNAL_SERVER_ERROR, ex.getHttpStatus());
            assertEquals(
                    "Error al acceder a la informacion del reporte de Aval",
                    ex.getMessage());
        }

        @Test
        @DisplayName("findReportStatus lanza excepcion si falla la consulta")
        void shouldThrowWhenLatestQueryFails() {
            when(reportRepository.countPendingMovements()).thenReturn(1);
            when(reportFileRepository.findLatest())
                    .thenThrow(new DataAccessResourceFailureException("db"));

            BusinessException ex = assertThrows(
                    BusinessException.class,
                    () -> service.findReportStatus(
                            CORRELATION_ID, REQUEST_ID));

            assertEquals(
                    HttpStatus.INTERNAL_SERVER_ERROR, ex.getHttpStatus());
        }

        @Test
        @DisplayName("generateAvalReport persiste el archivo generado")
        void shouldPersistGeneratedReport() throws IOException {
            byte[] content = new byte[] {0x50, 0x4B, 0x03, 0x04};

            when(storedProcedureExecutor.query(
                    anyString(),
                    any(StoredProcedureRowMapper.class),
                    anyString()))
                    .thenReturn(Collections.emptyList())
                    .thenReturn(Collections.singletonList(reportRow()));
            when(excelHelper.generateExcel(anyList())).thenReturn(content);
            when(reportFileRepository.save(any(ArchivoReporteAvalExcel.class)))
                    .thenReturn(reportFile());
            when(reportRepository.countPendingMovements()).thenReturn(93);

            AvalReportFileDTO result = service.generateAvalReport(
                    P_HEADER, CORRELATION_ID, REQUEST_ID);

            assertEquals(1, result.getId());
            assertEquals("RPT_CIERRE_AVAL.xlsx", result.getFileName());
            assertEquals(93, result.getPendingMovements());

            verify(reportFileRepository, times(1)).deleteAllFiles();
            verify(reportFileRepository, times(1))
                    .save(any(ArchivoReporteAvalExcel.class));
        }

        @Test
        @DisplayName("generateAvalReport persiste aunque no existan filas")
        void shouldPersistEvenWithoutRows() throws IOException {
            byte[] content = new byte[] {0x50, 0x4B};

            when(storedProcedureExecutor.query(
                    anyString(),
                    any(StoredProcedureRowMapper.class),
                    anyString()))
                    .thenReturn(Collections.emptyList());
            when(excelHelper.generateExcel(anyList())).thenReturn(content);
            when(reportFileRepository.save(any(ArchivoReporteAvalExcel.class)))
                    .thenReturn(reportFile());
            when(reportRepository.countPendingMovements()).thenReturn(0);

            AvalReportFileDTO result = service.generateAvalReport(
                    P_HEADER, CORRELATION_ID, REQUEST_ID);

            assertNotNull(result);
            assertEquals(0, result.getPendingMovements());
            verify(reportFileRepository, times(1))
                    .save(any(ArchivoReporteAvalExcel.class));
        }

        @Test
        @DisplayName("generateAvalReport lanza excepcion si falla el SP")
        void shouldThrowWhenProcedureFails() {
            when(storedProcedureExecutor.query(
                    anyString(),
                    any(StoredProcedureRowMapper.class),
                    anyString()))
                    .thenThrow(new DataAccessResourceFailureException("db"));

            BusinessException ex = assertThrows(
                    BusinessException.class,
                    () -> service.generateAvalReport(
                            P_HEADER, CORRELATION_ID, REQUEST_ID));

            assertEquals(
                    HttpStatus.INTERNAL_SERVER_ERROR, ex.getHttpStatus());
            verify(reportFileRepository, never()).deleteAllFiles();
        }

        @Test
        @DisplayName("generateAvalReport lanza excepcion si falla el Excel")
        void shouldThrowWhenExcelFails() throws IOException {
            when(storedProcedureExecutor.query(
                    anyString(),
                    any(StoredProcedureRowMapper.class),
                    anyString()))
                    .thenReturn(Collections.emptyList())
                    .thenReturn(Collections.singletonList(reportRow()));
            when(excelHelper.generateExcel(anyList()))
                    .thenThrow(new IOException("boom"));

            BusinessException ex = assertThrows(
                    BusinessException.class,
                    () -> service.generateAvalReport(
                            P_HEADER, CORRELATION_ID, REQUEST_ID));

            assertEquals(
                    HttpStatus.INTERNAL_SERVER_ERROR, ex.getHttpStatus());
            assertEquals(
                    "Error al generar el archivo Excel", ex.getMessage());
        }

        @Test
        @DisplayName("generateAvalReport lanza excepcion si falla el borrado")
        void shouldThrowWhenDeleteFails() throws IOException {
            when(storedProcedureExecutor.query(
                    anyString(),
                    any(StoredProcedureRowMapper.class),
                    anyString()))
                    .thenReturn(Collections.emptyList());
            when(excelHelper.generateExcel(anyList()))
                    .thenReturn(new byte[] {0x50});
            when(reportFileRepository.deleteAllFiles())
                    .thenThrow(new DataAccessResourceFailureException("db"));

            BusinessException ex = assertThrows(
                    BusinessException.class,
                    () -> service.generateAvalReport(
                            P_HEADER, CORRELATION_ID, REQUEST_ID));

            assertEquals(
                    HttpStatus.INTERNAL_SERVER_ERROR, ex.getHttpStatus());
        }

        @Test
        @DisplayName("generateAvalReport lanza excepcion si falla el guardado")
        void shouldThrowWhenSaveFails() throws IOException {
            when(storedProcedureExecutor.query(
                    anyString(),
                    any(StoredProcedureRowMapper.class),
                    anyString()))
                    .thenReturn(Collections.emptyList());
            when(excelHelper.generateExcel(anyList()))
                    .thenReturn(new byte[] {0x50});
            when(reportFileRepository.save(any(ArchivoReporteAvalExcel.class)))
                    .thenThrow(new DataAccessResourceFailureException("db"));

            BusinessException ex = assertThrows(
                    BusinessException.class,
                    () -> service.generateAvalReport(
                            P_HEADER, CORRELATION_ID, REQUEST_ID));

            assertEquals(
                    HttpStatus.INTERNAL_SERVER_ERROR, ex.getHttpStatus());
        }

        @Test
        @DisplayName("findReportFile devuelve el archivo solicitado")
        void shouldReturnRequestedReportFile() {
            when(reportFileRepository.findById(1))
                    .thenReturn(Optional.of(reportFile()));

            ArchivoReporteAvalExcel file =
                    service.findReportFile(1, CORRELATION_ID, REQUEST_ID);

            assertEquals(1, file.getId());
            assertEquals("RPT_CIERRE_AVAL.xlsx", file.getNombreArchivo());
        }

        @Test
        @DisplayName("findReportFile lanza excepcion si no existe")
        void shouldThrowWhenReportFileIsMissing() {
            when(reportFileRepository.findById(9))
                    .thenReturn(Optional.empty());

            BusinessException ex = assertThrows(
                    BusinessException.class,
                    () -> service.findReportFile(
                            9, CORRELATION_ID, REQUEST_ID));

            assertEquals(HttpStatus.NOT_FOUND, ex.getHttpStatus());
            assertEquals("El reporte solicitado no existe", ex.getMessage());
        }

        @Test
        @DisplayName("findReportFile lanza excepcion si no tiene contenido")
        void shouldThrowWhenReportContentIsMissing() {
            ArchivoReporteAvalExcel withoutContent = reportFile();
            withoutContent.setContenido(null);

            when(reportFileRepository.findById(1))
                    .thenReturn(Optional.of(withoutContent));

            BusinessException ex = assertThrows(
                    BusinessException.class,
                    () -> service.findReportFile(
                            1, CORRELATION_ID, REQUEST_ID));

            assertEquals(HttpStatus.NOT_FOUND, ex.getHttpStatus());
        }

        @Test
        @DisplayName("findReportFile lanza excepcion si falla la consulta")
        void shouldThrowWhenReportQueryFails() {
            when(reportFileRepository.findById(1))
                    .thenThrow(new DataAccessResourceFailureException("db"));

            BusinessException ex = assertThrows(
                    BusinessException.class,
                    () -> service.findReportFile(
                            1, CORRELATION_ID, REQUEST_ID));

            assertEquals(
                    HttpStatus.INTERNAL_SERVER_ERROR, ex.getHttpStatus());
        }
    }

    @Nested
    @DisplayName("Mapeo de resultados")
    class RowMapping {

        @SuppressWarnings("unchecked")
        private StoredProcedureRowMapper<ColombiaAccountingLine>
        captureAccountingMapper() {

            when(storedProcedureExecutor.query(
                    anyString(),
                    any(StoredProcedureRowMapper.class),
                    anyString()))
                    .thenReturn(Collections.emptyList());
            when(xmlHelper.buildFiles(anyList()))
                    .thenReturn(Collections.emptyList());

            assertThrows(
                    BusinessException.class,
                    () -> service.generateAccountingEntries(
                            P_HEADER, CORRELATION_ID, REQUEST_ID));

            ArgumentCaptor<StoredProcedureRowMapper<ColombiaAccountingLine>>
                    captor = ArgumentCaptor.forClass(
                    StoredProcedureRowMapper.class);

            verify(storedProcedureExecutor).query(
                    anyString(), captor.capture(), anyString());

            return captor.getValue();
        }

        @SuppressWarnings("unchecked")
        private StoredProcedureRowMapper<AvalReportRow> captureReportMapper()
                throws IOException {

            when(storedProcedureExecutor.query(
                    anyString(),
                    any(StoredProcedureRowMapper.class),
                    anyString()))
                    .thenReturn(Collections.emptyList());
            when(excelHelper.generateExcel(anyList()))
                    .thenReturn(new byte[] {0x50});
            when(reportFileRepository.save(any(ArchivoReporteAvalExcel.class)))
                    .thenReturn(new ArchivoReporteAvalExcel());
            when(reportRepository.countPendingMovements()).thenReturn(0);

            service.generateAvalReport(
                    P_HEADER, CORRELATION_ID, REQUEST_ID);

            ArgumentCaptor<StoredProcedureRowMapper<AvalReportRow>>
                    captor = ArgumentCaptor.forClass(
                    StoredProcedureRowMapper.class);

            verify(storedProcedureExecutor, times(2)).query(
                    anyString(), captor.capture(), anyString());

            return captor.getAllValues().get(1);
        }

        @Test
        @DisplayName("debe mapear la linea contable desde el ResultSet")
        void shouldMapAccountingLine() throws SQLException {
            StoredProcedureRowMapper<ColombiaAccountingLine> mapper =
                    captureAccountingMapper();

            ResultSet resultSet = mock(ResultSet.class);
            when(resultSet.getString("Familia")).thenReturn("ReasegAlfa");
            when(resultSet.getString("Periodo")).thenReturn("202608");
            when(resultSet.getInt("Pasada")).thenReturn(1);
            when(resultSet.getString("Mv")).thenReturn("Constitucion");
            when(resultSet.getString("NombreArchivo")).thenReturn(null);
            when(resultSet.getLong("Secuencia")).thenReturn(7L);
            when(resultSet.getString("Line")).thenReturn("<Line/>");

            ColombiaAccountingLine line = mapper.map(resultSet);

            assertEquals("ReasegAlfa", line.getFamily());
            assertEquals("202608", line.getPeriod());
            assertEquals(1, line.getPass());
            assertEquals("Constitucion", line.getMovementType());
            assertNull(line.getFileName());
            assertEquals(7L, line.getSequence());
            assertEquals("<Line/>", line.getContent());
        }

        @Test
        @DisplayName("debe mapear la fila del reporte desde el ResultSet")
        void shouldMapReportRow() throws Exception {
            StoredProcedureRowMapper<AvalReportRow> mapper =
                    captureReportMapper();

            ResultSet resultSet = mock(ResultSet.class);
            when(resultSet.getString(anyString())).thenReturn("valor");
            when(resultSet.getInt(anyString())).thenReturn(5);
            when(resultSet.getBigDecimal(anyString()))
                    .thenReturn(new java.math.BigDecimal("10.00"));
            when(resultSet.wasNull()).thenReturn(false);

            AvalReportRow row = mapper.map(resultSet);

            assertNotNull(row);
            assertEquals("valor", row.getCompania());
            assertEquals(5, row.getRamo2());
            assertEquals(
                    new java.math.BigDecimal("10.00"),
                    row.getValorPagos());
            assertEquals("valor", row.getObservacionesPago());
        }

        @Test
        @DisplayName("debe devolver null cuando el entero viene nulo")
        void shouldReturnNullWhenIntegerIsNull() throws Exception {
            StoredProcedureRowMapper<AvalReportRow> mapper =
                    captureReportMapper();

            ResultSet resultSet = mock(ResultSet.class);
            when(resultSet.getString(anyString())).thenReturn(null);
            when(resultSet.getInt(anyString())).thenReturn(0);
            when(resultSet.getBigDecimal(anyString())).thenReturn(null);
            when(resultSet.wasNull()).thenReturn(true);

            AvalReportRow row = mapper.map(resultSet);

            assertNotNull(row);
            assertNull(row.getRamo2());
            assertNull(row.getEdad());
            assertNull(row.getValorPagos());
        }

        @SuppressWarnings("unchecked")
        @Test
        @DisplayName("debe descartar el resultado del procedimiento de reporte")
        void shouldDiscardReportProcedureResult() throws Exception {
            when(storedProcedureExecutor.query(
                    anyString(),
                    any(StoredProcedureRowMapper.class),
                    anyString()))
                    .thenReturn(Collections.emptyList());
            when(excelHelper.generateExcel(anyList()))
                    .thenReturn(new byte[] {0x50});
            when(reportFileRepository.save(any(ArchivoReporteAvalExcel.class)))
                    .thenReturn(new ArchivoReporteAvalExcel());
            when(reportRepository.countPendingMovements()).thenReturn(0);

            service.generateAvalReport(
                    P_HEADER, CORRELATION_ID, REQUEST_ID);

            ArgumentCaptor<StoredProcedureRowMapper<Object>>
                    captor = ArgumentCaptor.forClass(
                    StoredProcedureRowMapper.class);

            verify(storedProcedureExecutor, times(2)).query(
                    anyString(), captor.capture(), anyString());

            StoredProcedureRowMapper<Object> mapper =
                    captor.getAllValues().get(0);

            assertNull(mapper.map(mock(ResultSet.class)));
        }
    }
}
