src/test/java/co/com/bnpparibas/cardif/closingclaims/domain/services/impl/PeruAccountingReportServiceImplTest.java

package co.com.bnpparibas.cardif.closingclaims.domain.services.impl;

import co.com.bnpparibas.cardif.closingclaims.domain.dtos.peruaccountingreport.PeruAccountingReportResponseDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.entity.PeruAccountingReport;
import co.com.bnpparibas.cardif.closingclaims.domain.util.exception.BusinessException;
import co.com.bnpparibas.cardif.closingclaims.domain.util.helpers.PeruAccountingReportExcelHelper;
import co.com.bnpparibas.cardif.closingclaims.domain.util.helpers.PeruAccountingReportMapper;
import co.com.bnpparibas.cardif.closingclaims.infraestructure.repository.PeruAccountingReportRepository;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.dao.DataAccessResourceFailureException;

import java.io.IOException;
import java.time.LocalDateTime;
import java.util.Collections;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertSame;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.Mockito.doNothing;
import static org.mockito.Mockito.doThrow;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.verifyNoInteractions;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class PeruAccountingReportServiceImplTest {

    private static final String P_HEADER = "test";
    private static final String CORRELATION_ID = "correlation-id";
    private static final String REQUEST_ID = "request-id";

    @Mock
    private PeruAccountingReportRepository repository;

    @Mock
    private PeruAccountingReportMapper mapper;

    @Mock
    private PeruAccountingReportExcelHelper excelHelper;

    @InjectMocks
    private PeruAccountingReportServiceImpl service;

    @Nested
    @DisplayName("Get latest report date")
    class GetLatestReportDate {

        @Test
        @DisplayName("Should return latest report date")
        void shouldReturnLatestReportDate() {
            LocalDateTime reportDate =
                    LocalDateTime.of(2026, 6, 15, 1, 56, 44);

            PeruAccountingReportResponseDTO expectedResponse =
                    PeruAccountingReportResponseDTO.builder()
                            .reportDate(reportDate)
                            .build();

            when(repository.findLatestReportDate())
                    .thenReturn(reportDate);

            when(mapper.toResponseDTO(reportDate))
                    .thenReturn(expectedResponse);

            PeruAccountingReportResponseDTO result =
                    service.getLatestReportDate(
                            P_HEADER,
                            CORRELATION_ID,
                            REQUEST_ID);

            assertSame(expectedResponse, result);
            verify(repository).findLatestReportDate();
            verify(mapper).toResponseDTO(reportDate);
        }

        @Test
        @DisplayName("Should throw BusinessException when report date does not exist")
        void shouldThrowExceptionWhenReportDateDoesNotExist() {
            when(repository.findLatestReportDate())
                    .thenReturn(null);

            assertThrows(
                    BusinessException.class,
                    () -> service.getLatestReportDate(
                            P_HEADER,
                            CORRELATION_ID,
                            REQUEST_ID));

            verify(repository).findLatestReportDate();
            verifyNoInteractions(mapper);
        }

        @Test
        @DisplayName("Should throw BusinessException when database query fails")
        void shouldThrowExceptionWhenDatabaseQueryFails() {
            when(repository.findLatestReportDate())
                    .thenThrow(new DataAccessResourceFailureException(
                            "Database error"));

            assertThrows(
                    BusinessException.class,
                    () -> service.getLatestReportDate(
                            P_HEADER,
                            CORRELATION_ID,
                            REQUEST_ID));

            verify(repository).findLatestReportDate();
            verifyNoInteractions(mapper);
        }
    }

    @Nested
    @DisplayName("Generate report")
    class GenerateReport {

        @Test
        @DisplayName("Should generate report successfully")
        void shouldGenerateReportSuccessfully() {
            doNothing()
                    .when(repository)
                    .generateReport();

            String result = service.generateReport(
                    P_HEADER,
                    CORRELATION_ID,
                    REQUEST_ID);

            assertEquals(
                    "Información del reporte contable generada correctamente.",
                    result);

            verify(repository).generateReport();
        }

        @Test
        @DisplayName("Should throw BusinessException when report generation fails")
        void shouldThrowExceptionWhenReportGenerationFails() {
            doThrow(new DataAccessResourceFailureException(
                    "Stored procedure error"))
                    .when(repository)
                    .generateReport();

            assertThrows(
                    BusinessException.class,
                    () -> service.generateReport(
                            P_HEADER,
                            CORRELATION_ID,
                            REQUEST_ID));

            verify(repository).generateReport();
        }
    }

    @Nested
    @DisplayName("Download report")
    class DownloadReport {

        @Test
        @DisplayName("Should generate Excel successfully")
        void shouldGenerateExcelSuccessfully() throws IOException {
            PeruAccountingReport report =
                    PeruAccountingReport.builder().build();

            List<PeruAccountingReport> reports =
                    Collections.singletonList(report);

            byte[] expectedFile = new byte[]{1, 2, 3};

            when(repository.findAllForExport())
                    .thenReturn(reports);

            when(excelHelper.generateExcel(reports))
                    .thenReturn(expectedFile);

            byte[] result = service.downloadReport(
                    P_HEADER,
                    CORRELATION_ID,
                    REQUEST_ID);

            assertArrayEquals(expectedFile, result);
            verify(repository).findAllForExport();
            verify(excelHelper).generateExcel(reports);
        }

        @Test
        @DisplayName("Should throw BusinessException when report list is empty")
        void shouldThrowExceptionWhenReportListIsEmpty() {
            when(repository.findAllForExport())
                    .thenReturn(Collections.emptyList());

            assertThrows(
                    BusinessException.class,
                    () -> service.downloadReport(
                            P_HEADER,
                            CORRELATION_ID,
                            REQUEST_ID));

            verify(repository).findAllForExport();
            verifyNoInteractions(excelHelper);
        }

        @Test
        @DisplayName("Should throw BusinessException when report list is null")
        void shouldThrowExceptionWhenReportListIsNull() {
            when(repository.findAllForExport())
                    .thenReturn(null);

            assertThrows(
                    BusinessException.class,
                    () -> service.downloadReport(
                            P_HEADER,
                            CORRELATION_ID,
                            REQUEST_ID));

            verify(repository).findAllForExport();
            verifyNoInteractions(excelHelper);
        }

        @Test
        @DisplayName("Should throw BusinessException when database query fails")
        void shouldThrowExceptionWhenDatabaseQueryFails() {
            when(repository.findAllForExport())
                    .thenThrow(new DataAccessResourceFailureException(
                            "Database error"));

            assertThrows(
                    BusinessException.class,
                    () -> service.downloadReport(
                            P_HEADER,
                            CORRELATION_ID,
                            REQUEST_ID));

            verify(repository).findAllForExport();
            verifyNoInteractions(excelHelper);
        }

        @Test
        @DisplayName("Should throw BusinessException when Excel generation fails")
        void shouldThrowExceptionWhenExcelGenerationFails()
                throws IOException {

            PeruAccountingReport report =
                    PeruAccountingReport.builder().build();

            List<PeruAccountingReport> reports =
                    Collections.singletonList(report);

            when(repository.findAllForExport())
                    .thenReturn(reports);

            when(excelHelper.generateExcel(reports))
                    .thenThrow(new IOException("Excel error"));

            assertThrows(
                    BusinessException.class,
                    () -> service.downloadReport(
                            P_HEADER,
                            CORRELATION_ID,
                            REQUEST_ID));

            verify(repository).findAllForExport();
            verify(excelHelper).generateExcel(reports);
        }
    }
}
