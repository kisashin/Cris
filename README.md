package co.com.bnpparibas.cardif.closingclaims.api;

import co.com.bnpparibas.cardif.closingclaims.domain.dtos.cardifcenterclosing.AccountingXmlFileDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.cardifcenterclosing.CenterAccountingResultDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.response.model.ResponseModel;
import co.com.bnpparibas.cardif.closingclaims.domain.entity.ArchivoAsientoCentro;
import co.com.bnpparibas.cardif.closingclaims.domain.services.ICardifCenterClosingService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.test.util.ReflectionTestUtils;

import java.nio.charset.StandardCharsets;
import java.util.Collections;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class CardifCenterClosingControllerTest {

    private static final String P_HEADER = "test";
    private static final String CORRELATION_ID = "correlation-id";
    private static final String REQUEST_ID = "request-id";
    private static final String FILE_NAME = "ReporteMovimientosCentro.xlsx";
    private static final String XML_NAME =
            "Sinie_ReasegCentro_Pago20260824.xml";

    @Mock
    private ICardifCenterClosingService service;

    @InjectMocks
    private CardifCenterClosingController controller;

    @BeforeEach
    void setUp() {
        ReflectionTestUtils.setField(controller, "fileName", FILE_NAME);
    }

    private AccountingXmlFileDTO fileDto() {
        return AccountingXmlFileDTO.builder()
                .id(1)
                .period("202608")
                .movementType("Pago")
                .fileName(XML_NAME)
                .lineCount(2)
                .processDate("24/08/2026 03:03:29 p. m.")
                .status("GENERADO")
                .build();
    }

    @Nested
    @DisplayName("Generate accounting entries")
    class GenerateAccountingEntries {

        @Test
        @DisplayName("Should return the generated files")
        void shouldReturnGeneratedFiles() {
            CenterAccountingResultDTO expected =
                    CenterAccountingResultDTO.builder()
                            .message("Asientos generados con éxito.")
                            .period("202608")
                            .files(Collections.singletonList(fileDto()))
                            .build();

            when(service.generateAccountingEntries(
                    P_HEADER, CORRELATION_ID, REQUEST_ID))
                    .thenReturn(expected);

            ResponseEntity<ResponseModel<CenterAccountingResultDTO>> response =
                    controller.generateAccountingEntries(
                            P_HEADER, CORRELATION_ID, REQUEST_ID);

            assertEquals(HttpStatus.OK, response.getStatusCode());
            assertNotNull(response.getBody());
            assertEquals(expected, response.getBody().getBodyResponse());

            verify(service).generateAccountingEntries(
                    P_HEADER, CORRELATION_ID, REQUEST_ID);
        }
    }

    @Nested
    @DisplayName("Find generated files")
    class FindGeneratedFiles {

        @Test
        @DisplayName("Should return the persisted files")
        void shouldReturnPersistedFiles() {
            List<AccountingXmlFileDTO> expected =
                    Collections.singletonList(fileDto());

            when(service.findGeneratedFiles(CORRELATION_ID, REQUEST_ID))
                    .thenReturn(expected);

            ResponseEntity<ResponseModel<List<AccountingXmlFileDTO>>> response =
                    controller.findGeneratedFiles(CORRELATION_ID, REQUEST_ID);

            assertEquals(HttpStatus.OK, response.getStatusCode());
            assertNotNull(response.getBody());
            assertEquals(expected, response.getBody().getBodyResponse());
        }
    }

    @Nested
    @DisplayName("Download XML file")
    class DownloadXmlFile {

        @Test
        @DisplayName("Should stream the XML content as an attachment")
        void shouldStreamXmlContent() {
            ArchivoAsientoCentro file = ArchivoAsientoCentro.builder()
                    .id(1)
                    .nombreArchivo(XML_NAME)
                    .contenido("<SSC/>")
                    .build();

            when(service.findXmlFile(1, CORRELATION_ID, REQUEST_ID))
                    .thenReturn(file);

            ResponseEntity<byte[]> response = controller.downloadXmlFile(
                    1, CORRELATION_ID, REQUEST_ID);

            assertEquals(HttpStatus.OK, response.getStatusCode());
            assertArrayEquals(
                    "<SSC/>".getBytes(StandardCharsets.UTF_8),
                    response.getBody());
            assertEquals(
                    "attachment; filename=\"" + XML_NAME + "\"",
                    response.getHeaders()
                            .getFirst(HttpHeaders.CONTENT_DISPOSITION));
            assertEquals(
                    "application/xml",
                    response.getHeaders().getContentType().toString());
        }
    }

    @Nested
    @DisplayName("Download movements report")
    class DownloadMovementsReport {

        @Test
        @DisplayName("Should download Excel report successfully")
        void shouldDownloadExcelReportSuccessfully() {
            byte[] expectedFile = new byte[]{1, 2, 3, 4};

            when(service.downloadMovementsReport(
                    P_HEADER, CORRELATION_ID, REQUEST_ID))
                    .thenReturn(expectedFile);

            ResponseEntity<byte[]> response =
                    controller.downloadMovementsReport(
                            P_HEADER, CORRELATION_ID, REQUEST_ID);

            assertEquals(HttpStatus.OK, response.getStatusCode());
            assertArrayEquals(expectedFile, response.getBody());
            assertEquals(
                    "attachment; filename=\"" + FILE_NAME + "\"",
                    response.getHeaders()
                            .getFirst(HttpHeaders.CONTENT_DISPOSITION));
            assertEquals(
                    expectedFile.length,
                    response.getHeaders().getContentLength());
        }
    }
}
