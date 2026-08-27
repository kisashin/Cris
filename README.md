import java.nio.charset.StandardCharsets;
import java.util.Collections;

import co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia.ColombiaAccountingResultDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia.ColombiaXmlFileDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.entity.ArchivoAsientoAvalXml;
import org.junit.jupiter.api.Nested;
import org.springframework.http.HttpHeaders;

    @Nested
    @DisplayName("PUT /v1/aval-closing/generate")
    class GenerateAccountingEntries {

        @Test
        @DisplayName("debe devolver el resultado del proceso y código 200")
        void shouldReturnGenerationResult() {
            ColombiaAccountingResultDTO serviceResult =
                    ColombiaAccountingResultDTO.builder()
                            .message("Asientos generados con éxito.")
                            .period("202608")
                            .files(Collections.emptyList())
                            .build();

            when(closingAvalService.generateAccountingEntries(
                    pHeader, correlationId, requestId))
                    .thenReturn(serviceResult);

            ResponseEntity<ResponseModel<ColombiaAccountingResultDTO>> response =
                    controller.generateAccountingEntries(
                            pHeader, correlationId, requestId);

            assertEquals(HttpStatus.OK, response.getStatusCode());

            ResponseModel<ColombiaAccountingResultDTO> body = response.getBody();
            assertNotNull(body);
            assertEquals(correlationId, body.getCorrelationId());
            assertEquals(
                    HttpStatus.OK.value(),
                    body.getResponseHeader().getReturnCode());
            assertEquals(serviceResult, body.getBodyResponse());

            verify(closingAvalService, times(1))
                    .generateAccountingEntries(
                            pHeader, correlationId, requestId);
        }
    }

    @Nested
    @DisplayName("GET /v1/aval-closing/files")
    class FindGeneratedFiles {

        @Test
        @DisplayName("debe devolver los archivos generados y código 200")
        void shouldReturnGeneratedFiles() {
            List<ColombiaXmlFileDTO> serviceResult = Collections.singletonList(
                    ColombiaXmlFileDTO.builder()
                            .id(1)
                            .family("ReasegAlfa")
                            .fileName("archivo.xml")
                            .build());

            when(closingAvalService.findGeneratedFiles(
                    correlationId, requestId))
                    .thenReturn(serviceResult);

            ResponseEntity<ResponseModel<List<ColombiaXmlFileDTO>>> response =
                    controller.findGeneratedFiles(correlationId, requestId);

            assertEquals(HttpStatus.OK, response.getStatusCode());

            ResponseModel<List<ColombiaXmlFileDTO>> body = response.getBody();
            assertNotNull(body);
            assertEquals(correlationId, body.getCorrelationId());
            assertEquals(serviceResult, body.getBodyResponse());

            verify(closingAvalService, times(1))
                    .findGeneratedFiles(correlationId, requestId);
        }
    }

    @Nested
    @DisplayName("GET /v1/aval-closing/files/{id}/download")
    class DownloadXmlFile {

        @Test
        @DisplayName("debe devolver el contenido del archivo con su nombre")
        void shouldReturnFileContent() {
            String content = "<SSC><Line/></SSC>";

            ArchivoAsientoAvalXml file = ArchivoAsientoAvalXml.builder()
                    .id(1)
                    .nombreArchivo("ReasegAlf_HogarPago20260827.xml")
                    .contenido(content)
                    .build();

            when(closingAvalService.findXmlFile(
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
                            + "ReasegAlf_HogarPago20260827.xml\"",
                    response.getHeaders()
                            .getFirst(HttpHeaders.CONTENT_DISPOSITION));

            verify(closingAvalService, times(1))
                    .findXmlFile(1, correlationId, requestId);
        }
    }
