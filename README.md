package co.com.bnpparibas.cardif.closingclaims.api;

import co.com.bnpparibas.cardif.closingclaims.domain.dtos.cardifcenterclosing.AccountingXmlFileDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.cardifcenterclosing.CenterAccountingResultDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.response.model.ResponseModel;
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

import java.util.Collections;

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

    @Mock
    private ICardifCenterClosingService service;

    @InjectMocks
    private CardifCenterClosingController controller;

    @BeforeEach
    void setUp() {
        ReflectionTestUtils.setField(controller, "fileName", FILE_NAME);
    }

    @Nested
    @DisplayName("Generate accounting entries")
    class GenerateAccountingEntries {

        @Test
        @DisplayName("Should return the generated XML files")
        void shouldReturnGeneratedXmlFiles() {
            CenterAccountingResultDTO expected =
                    CenterAccountingResultDTO.builder()
                            .message("Asientos generados con éxito.")
                            .status("PROCESADO")
                            .period("202608")
                            .processDate("24/08/2026 03:03:29 p. m.")
                            .files(Collections.singletonList(
                                    AccountingXmlFileDTO.builder()
                                            .movementType("Pago")
                                            .fileName("Sinie_ReasegCentro_Pago20260824.xml")
                                            .lineCount(2)
                                            .content("Y29udGVudA==")
                                            .build()))
                            .build();

            when(service.generateAccountingEntries(
                    P_HEADER, CORRELATION_ID, REQUEST_ID))
                    .thenReturn(expected);

            ResponseEntity<ResponseModel<CenterAccountingResultDTO>> response =
                    controller.generateAccountingEntries(
                            P_HEADER, CORRELATION_ID, REQUEST_ID);

            assertEquals(HttpStatus.OK, response.getStatusCode());
            assertNotNull(response.getBody());
            assertEquals(
                    expected,
                    response.getBody().getBodyResponse());

            verify(service).generateAccountingEntries(
                    P_HEADER, CORRELATION_ID, REQUEST_ID);
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

            verify(service).downloadMovementsReport(
                    P_HEADER, CORRELATION_ID, REQUEST_ID);
        }
    }
}
