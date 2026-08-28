import java.io.IOException;

import co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia.AvalReportRow;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia.AvalReportStatusDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.util.helpers.AvalReportExcelHelper;
import co.com.bnpparibas.cardif.closingclaims.infraestructure.repository.AvalReportRepository;


    @Mock
    private AvalReportRepository reportRepository;

    @Mock
    private AvalReportExcelHelper excelHelper;








        @Nested
    @DisplayName("findReportStatus")
    class FindReportStatus {

        @Test
        @DisplayName("debe devolver el conteo de movimientos pendientes")
        void shouldReturnPendingCount() {
            when(reportRepository.countPendingMovements()).thenReturn(93);

            AvalReportStatusDTO status =
                    service.findReportStatus(CORRELATION_ID, REQUEST_ID);

            assertEquals(93, status.getPendingMovements());
            assertNotNull(status.getGenerationDate());
        }

        @Test
        @DisplayName("debe devolver cero cuando no hay movimientos pendientes")
        void shouldReturnZeroWhenThereAreNoPendingMovements() {
            when(reportRepository.countPendingMovements()).thenReturn(0);

            AvalReportStatusDTO status =
                    service.findReportStatus(CORRELATION_ID, REQUEST_ID);

            assertEquals(0, status.getPendingMovements());
            assertNotNull(status.getGenerationDate());
        }

        @Test
        @DisplayName("debe lanzar BusinessException cuando falla la consulta")
        void shouldThrowWhenQueryFails() {
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
    }

    @Nested
    @DisplayName("downloadAvalReport")
    class DownloadAvalReport {

        private AvalReportRow reportRow() {
            return AvalReportRow.builder()
                    .compania("02")
                    .siniestroLider("0902026A193877")
                    .nombreasegurado("JUAN PEREZ")
                    .build();
        }

        @Test
        @DisplayName("debe devolver el contenido del archivo Excel")
        void shouldReturnExcelContent() throws IOException {
            byte[] expected = new byte[] {0x50, 0x4B, 0x03, 0x04};

            when(storedProcedureExecutor.query(
                    anyString(),
                    any(StoredProcedureRowMapper.class),
                    anyString()))
                    .thenReturn(Collections.emptyList())
                    .thenReturn(Collections.singletonList(reportRow()));
            when(excelHelper.generateExcel(anyList()))
                    .thenReturn(expected);

            byte[] result = service.downloadAvalReport(
                    P_HEADER, CORRELATION_ID, REQUEST_ID);

            assertArrayEquals(expected, result);

            verify(storedProcedureExecutor, times(2)).query(
                    anyString(),
                    any(StoredProcedureRowMapper.class),
                    anyString());
        }

        @Test
        @DisplayName("debe lanzar BusinessException cuando no hay movimientos")
        void shouldThrowWhenThereAreNoRows() {
            when(storedProcedureExecutor.query(
                    anyString(),
                    any(StoredProcedureRowMapper.class),
                    anyString()))
                    .thenReturn(Collections.emptyList());

            BusinessException ex = assertThrows(
                    BusinessException.class,
                    () -> service.downloadAvalReport(
                            P_HEADER, CORRELATION_ID, REQUEST_ID));

            assertEquals(HttpStatus.NOT_FOUND, ex.getHttpStatus());
            assertEquals(
                    "No existen movimientos para generar el archivo",
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
                    () -> service.downloadAvalReport(
                            P_HEADER, CORRELATION_ID, REQUEST_ID));

            assertEquals(
                    HttpStatus.INTERNAL_SERVER_ERROR, ex.getHttpStatus());
            assertEquals(
                    "Error al acceder a la informacion del reporte de Aval",
                    ex.getMessage());
        }

        @Test
        @DisplayName("debe lanzar BusinessException cuando falla la generacion del Excel")
        void shouldThrowWhenExcelGenerationFails() throws IOException {
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
                    () -> service.downloadAvalReport(
                            P_HEADER, CORRELATION_ID, REQUEST_ID));

            assertEquals(
                    HttpStatus.INTERNAL_SERVER_ERROR, ex.getHttpStatus());
            assertEquals(
                    "Error al generar el archivo Excel",
                    ex.getMessage());
        }
    }
