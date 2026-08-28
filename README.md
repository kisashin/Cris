import co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia.AvalReportStatusDTO;


    @Nested
    @DisplayName("GET /v1/aval-closing/report/status")
    class FindReportStatus {

        @Test
        @DisplayName("debe devolver el estado del reporte y código 200")
        void shouldReturnReportStatus() {
            AvalReportStatusDTO serviceResult =
                    AvalReportStatusDTO.builder()
                            .generationDate("27/08/2026 10:00:00 a. m.")
                            .pendingMovements(93)
                            .build();

            when(closingAvalService.findReportStatus(
                    correlationId, requestId))
                    .thenReturn(serviceResult);

            ResponseEntity<ResponseModel<AvalReportStatusDTO>> response =
                    controller.findReportStatus(correlationId, requestId);

            assertEquals(HttpStatus.OK, response.getStatusCode());

            ResponseModel<AvalReportStatusDTO> body = response.getBody();
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
        @DisplayName("debe devolver cero movimientos cuando no hay pendientes")
        void shouldReturnZeroPendingMovements() {
            AvalReportStatusDTO serviceResult =
                    AvalReportStatusDTO.builder()
                            .generationDate("27/08/2026 10:00:00 a. m.")
                            .pendingMovements(0)
                            .build();

            when(closingAvalService.findReportStatus(
                    correlationId, requestId))
                    .thenReturn(serviceResult);

            ResponseEntity<ResponseModel<AvalReportStatusDTO>> response =
                    controller.findReportStatus(correlationId, requestId);

            assertEquals(HttpStatus.OK, response.getStatusCode());

            ResponseModel<AvalReportStatusDTO> body = response.getBody();
            assertNotNull(body);
            assertEquals(0, body.getBodyResponse().getPendingMovements());
        }
    }

    @Nested
    @DisplayName("GET /v1/aval-closing/report/download")
    class DownloadAvalReport {

        @Test
        @DisplayName("debe devolver el contenido del archivo con su nombre")
        void shouldReturnReportContent() {
            byte[] content = new byte[] {0x50, 0x4B, 0x03, 0x04};

            when(closingAvalService.downloadAvalReport(
                    pHeader, correlationId, requestId))
                    .thenReturn(content);

            ResponseEntity<byte[]> response =
                    controller.downloadAvalReport(
                            pHeader, correlationId, requestId);

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
                    .downloadAvalReport(pHeader, correlationId, requestId);
        }
    }
