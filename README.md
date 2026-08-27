import java.nio.charset.StandardCharsets;

import co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia.ColombiaAccountingResultDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia.ColombiaXmlFileDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.entity.ArchivoAsientoCardifXml;
import org.springframework.http.HttpHeaders;

    @Nested
    @DisplayName("PUT /v1/cardif-closing/generate")
    class GenerateAccountingEntries {

        @Test
        @DisplayName("debe devolver el resultado del proceso y código 200")
        void shouldReturnGenerationResult() {
            String correlationId = "corr-gen";
            String requestId = "req-gen";

            ColombiaAccountingResultDTO serviceResult =
                    ColombiaAccountingResultDTO.builder()
                            .message("Asientos generados con éxito.")
                            .period("202608")
                            .files(Collections.emptyList())
                            .build();

            when(closingCardifService.generateAccountingEntries(
                    "hdr", correlationId, requestId))
                    .thenReturn(serviceResult);

            ResponseEntity<ResponseModel<ColombiaAccountingResultDTO>> response =
                    controller.generateAccountingEntries(
                            "hdr", correlationId, requestId);

            assertEquals(HttpStatus.OK, response.getStatusCode());

            ResponseModel<ColombiaAccountingResultDTO> body = response.getBody();
            assertNotNull(body);
            assertEquals(correlationId, body.getCorrelationId());
            assertEquals(
                    HttpStatus.OK.value(),
                    body.getResponseHeader().getReturnCode());
            assertEquals(serviceResult, body.getBodyResponse());

            verify(closingCardifService, times(1))
                    .generateAccountingEntries("hdr", correlationId, requestId);
        }
    }

    @Nested
    @DisplayName("GET /v1/cardif-closing/files")
    class FindGeneratedFiles {

        @Test
        @DisplayName("debe devolver los archivos generados y código 200")
        void shouldReturnGeneratedFiles() {
            String correlationId = "corr-files";
            String requestId = "req-files";

            List<ColombiaXmlFileDTO> serviceResult = Collections.singletonList(
                    ColombiaXmlFileDTO.builder()
                            .id(1)
                            .family("ReasegCardif")
                            .fileName("archivo.xml")
                            .build());

            when(closingCardifService.findGeneratedFiles(
                    correlationId, requestId))
                    .thenReturn(serviceResult);

            ResponseEntity<ResponseModel<List<ColombiaXmlFileDTO>>> response =
                    controller.findGeneratedFiles(correlationId, requestId);

            assertEquals(HttpStatus.OK, response.getStatusCode());

            ResponseModel<List<ColombiaXmlFileDTO>> body = response.getBody();
            assertNotNull(body);
            assertEquals(correlationId, body.getCorrelationId());
            assertEquals(serviceResult, body.getBodyResponse());

            verify(closingCardifService, times(1))
                    .findGeneratedFiles(correlationId, requestId);
        }
    }

    @Nested
    @DisplayName("GET /v1/cardif-closing/files/{id}/download")
    class DownloadXmlFile {

        @Test
        @DisplayName("debe devolver el contenido del archivo con su nombre")
        void shouldReturnFileContent() {
            String correlationId = "corr-download";
            String requestId = "req-download";
            String content = "<SSC><Line/></SSC>";

            ArchivoAsientoCardifXml file = ArchivoAsientoCardifXml.builder()
                    .id(1)
                    .nombreArchivo("ReasegDirectasPago20260827.xml")
                    .contenido(content)
                    .build();

            when(closingCardifService.findXmlFile(
                    1, correlationId, requestId))
                    .thenReturn(file);

            ResponseEntity<byte[]> response = controller.downloadXmlFile(
                    1, correlationId, requestId);

            assertEquals(HttpStatus.OK, response.getStatusCode());
            assertArrayEquals(
                    content.getBytes(StandardCharsets.UTF_8),
                    response.getBody());
            assertEquals(
                    "attachment; filename=\""
                            + "ReasegDirectasPago20260827.xml\"",
                    response.getHeaders()
                            .getFirst(HttpHeaders.CONTENT_DISPOSITION));
            assertEquals(
                    content.getBytes(StandardCharsets.UTF_8).length,
                    response.getHeaders().getContentLength());

            verify(closingCardifService, times(1))
                    .findXmlFile(1, correlationId, requestId);
        }
    }
