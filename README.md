src/test/java/co/com/bnpparibas/cardif/closingclaims/api/PeruAccountingReportControllerTest.java

package co.com.bnpparibas.cardif.closingclaims.api;

import co.com.bnpparibas.cardif.closingclaims.domain.dtos.peruaccountingreport.PeruAccountingReportResponseDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.services.IPeruAccountingReportService;
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

import java.time.LocalDateTime;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class PeruAccountingReportControllerTest {

    private static final String P_HEADER = "test";
    private static final String CORRELATION_ID = "correlation-id";
    private static final String REQUEST_ID = "request-id";

    @Mock
    private IPeruAccountingReportService service;

    @InjectMocks
    private PeruAccountingReportController controller;

    @Nested
    @DisplayName("Get latest report date")
    class GetLatestReportDate {

        @Test
        @DisplayName("Should return latest report date successfully")
        void shouldReturnLatestReportDateSuccessfully() {
            PeruAccountingReportResponseDTO responseDTO =
                    PeruAccountingReportResponseDTO.builder()
                            .reportDate(LocalDateTime.of(
                                    2026,
                                    6,
                                    15,
                                    1,
                                    56,
                                    44))
                            .build();

            when(service.getLatestReportDate(
                    P_HEADER,
                    CORRELATION_ID,
                    REQUEST_ID))
                    .thenReturn(responseDTO);

            ResponseEntity<?> response =
                    controller.getLatestReportDate(
                            P_HEADER,
                            CORRELATION_ID,
                            REQUEST_ID);

            assertEquals(HttpStatus.OK, response.getStatusCode());
            assertNotNull(response.getBody());

            verify(service).getLatestReportDate(
                    P_HEADER,
                    CORRELATION_ID,
                    REQUEST_ID);
        }
    }

    @Nested
    @DisplayName("Generate report")
    class GenerateReport {

        @Test
        @DisplayName("Should generate report successfully")
        void shouldGenerateReportSuccessfully() {
            String expectedMessage =
                    "Información del reporte contable generada correctamente.";

            when(service.generateReport(
                    P_HEADER,
                    CORRELATION_ID,
                    REQUEST_ID))
                    .thenReturn(expectedMessage);

            ResponseEntity<?> response =
                    controller.generateReport(
                            P_HEADER,
                            CORRELATION_ID,
                            REQUEST_ID);

            assertEquals(HttpStatus.OK, response.getStatusCode());
            assertNotNull(response.getBody());

            verify(service).generateReport(
                    P_HEADER,
                    CORRELATION_ID,
                    REQUEST_ID);
        }
    }

    @Nested
    @DisplayName("Download report")
    class DownloadReport {

        @Test
        @DisplayName("Should download Excel report successfully")
        void shouldDownloadExcelReportSuccessfully() {
            byte[] expectedFile = new byte[]{1, 2, 3, 4};

            when(service.downloadReport(
                    P_HEADER,
                    CORRELATION_ID,
                    REQUEST_ID))
                    .thenReturn(expectedFile);

            ResponseEntity<byte[]> response =
                    controller.downloadReport(
                            P_HEADER,
                            CORRELATION_ID,
                            REQUEST_ID);

            assertEquals(HttpStatus.OK, response.getStatusCode());
            assertArrayEquals(expectedFile, response.getBody());

            assertEquals(
                    "attachment; filename=\"ReporteContablePeru.xlsx\"",
                    response.getHeaders()
                            .getFirst(HttpHeaders.CONTENT_DISPOSITION));

            assertEquals(
                    expectedFile.length,
                    response.getHeaders().getContentLength());

            assertEquals(
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    response.getHeaders()
                            .getContentType()
                            .toString());

            verify(service).downloadReport(
                    P_HEADER,
                    CORRELATION_ID,
                    REQUEST_ID);
        }
    }
}
