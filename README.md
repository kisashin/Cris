CardifCenterClosingControllerTest

package co.com.bnpparibas.cardif.closingclaims.api;

import co.com.bnpparibas.cardif.closingclaims.domain.services.ICardifCenterClosingService;
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

    @Mock
    private ICardifCenterClosingService service;

    @InjectMocks
    private CardifCenterClosingController controller;

    @Nested
    @DisplayName("Generate accounting entries")
    class GenerateAccountingEntries {

        @Test
        @DisplayName("Should generate accounting entries successfully")
        void shouldGenerateAccountingEntriesSuccessfully() {
            String expectedMessage = "Asientos generados con éxito.";

            when(service.generateAccountingEntries(
                    P_HEADER, CORRELATION_ID, REQUEST_ID))
                    .thenReturn(expectedMessage);

            ResponseEntity<?> response =
                    controller.generateAccountingEntries(
                            P_HEADER, CORRELATION_ID, REQUEST_ID);

            assertEquals(HttpStatus.OK, response.getStatusCode());
            assertNotNull(response.getBody());

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
                    "attachment; filename=\"ReporteMovimientosCentro.xlsx\"",
                    response.getHeaders()
                            .getFirst(HttpHeaders.CONTENT_DISPOSITION));

            assertEquals(
                    expectedFile.length,
                    response.getHeaders().getContentLength());

            assertEquals(
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    response.getHeaders().getContentType().toString());

            verify(service).downloadMovementsReport(
                    P_HEADER, CORRELATION_ID, REQUEST_ID);
        }
    }
}
