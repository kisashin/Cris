import co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia.AvalReportFileDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.entity.ArchivoReporteAvalExcel;


    @Nested
    @DisplayName("GET /v1/aval-closing/report/status")
    class FindReportStatus {

        @Test
        @DisplayName("debe devolver el estado del reporte y código 200")
        void shouldReturnReportStatus() {
            AvalReportFileDTO serviceResult = AvalReportFileDTO.builder()
                    .id(1)
                    .period("202609")
                    .fileName("RPT_CIERRE_AVAL.xlsx")
                    .rowCount(257)
                    .processDate("09/09/2026 10:00:00 a. m.")
                    .status("GENERADO")
                    .pendingMovements(93)
                    .build();

            when(closingAvalService.findReportStatus(
                    correlationId, requestId))
                    .thenReturn(serviceResult);

            ResponseEntity<ResponseModel<AvalReportFileDTO>> response =
                    controller.findReportStatus(correlationId, requestId);

            assertEquals(HttpStatus.OK, response.getStatusCode());

            ResponseModel<AvalReportFileDTO> body = response.getBody();
            assertNotNull(body);
            assertEquals(correlationId, body.getCorrelationId());
            assertEquals(
                    HttpStatus.OK.value(),
                    body.getResponseHeader().getReturnCode());
            assertEquals(serviceResult, body.getBodyResponse());

            verify(closingAvalService, times(1))
                    .findReportStatus(correlationId, requestId);
        }

        @Test
        @DisplayName("debe devolver el estado sin archivo generado")
        void shouldReturnStatusWithoutFile() {
            AvalReportFileDTO serviceResult = AvalReportFileDTO.builder()
                    .pendingMovements(0)
                    .build();

            when(closingAvalService.findReportStatus(
                    correlationId, requestId))
                    .thenReturn(serviceResult);

            ResponseEntity<ResponseModel<AvalReportFileDTO>> response =
                    controller.findReportStatus(correlationId, requestId);

            assertEquals(HttpStatus.OK, response.getStatusCode());
            assertNull(response.getBody().getBodyResponse().getId());
        }
    }

    @Nested
    @DisplayName("PUT /v1/aval-closing/report/generate")
    class GenerateAvalReport {

        @Test
        @DisplayName("debe devolver el reporte generado y código 200")
        void shouldReturnGeneratedReport() {
            AvalReportFileDTO serviceResult = AvalReportFileDTO.builder()
                    .id(1)
                    .fileName("RPT_CIERRE_AVAL.xlsx")
                    .rowCount(257)
                    .pendingMovements(93)
                    .build();

            when(closingAvalService.generateAvalReport(
                    pHeader, correlationId, requestId))
                    .thenReturn(serviceResult);

            ResponseEntity<ResponseModel<AvalReportFileDTO>> response =
                    controller.generateAvalReport(
                            pHeader, correlationId, requestId);

            assertEquals(HttpStatus.OK, response.getStatusCode());

            ResponseModel<AvalReportFileDTO> body = response.getBody();
            assertNotNull(body);
            assertEquals(
                    HttpStatus.OK.value(),
                    body.getResponseHeader().getReturnCode());
            assertEquals(serviceResult, body.getBodyResponse());

            verify(closingAvalService, times(1))
                    .generateAvalReport(pHeader, correlationId, requestId);
        }
    }

    @Nested
    @DisplayName("GET /v1/aval-closing/report/{id}/download")
    class DownloadAvalReport {

        @Test
        @DisplayName("debe devolver el contenido del archivo con su nombre")
        void shouldReturnReportContent() {
            byte[] content = new byte[] {0x50, 0x4B, 0x03, 0x04};

            ArchivoReporteAvalExcel file = ArchivoReporteAvalExcel.builder()
                    .id(1)
                    .nombreArchivo("RPT_CIERRE_AVAL.xlsx")
                    .contenido(content)
                    .build();

            when(closingAvalService.findReportFile(
                    1, correlationId, requestId))
                    .thenReturn(file);

            ResponseEntity<byte[]> response =
                    controller.downloadAvalReport(
                            1, correlationId, requestId);

            assertEquals(HttpStatus.OK, response.getStatusCode());
            assertArrayEquals(content, response.getBody());
            assertEquals(
                    "attachment; filename=\"RPT_CIERRE_AVAL.xlsx\"",
                    response.getHeaders()
                            .getFirst(HttpHeaders.CONTENT_DISPOSITION));
            assertEquals(
                    content.length,
                    response.getHeaders().getContentLength());

            verify(closingAvalService, times(1))
                    .findReportFile(1, correlationId, requestId);
        }
    }
