CardifPeruClosingServiceImplTest

package co.com.bnpparibas.cardif.closingclaims.domain.services.impl;

import co.com.bnpparibas.cardif.closingclaims.domain.entity.CardifPeruClosing;
import co.com.bnpparibas.cardif.closingclaims.domain.util.exception.BusinessException;
import co.com.bnpparibas.cardif.closingclaims.domain.util.helpers.CardifPeruClosingExcelHelper;
import co.com.bnpparibas.cardif.closingclaims.infraestructure.repository.CardifPeruClosingRepository;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.dao.DataAccessResourceFailureException;

import java.io.IOException;
import java.util.Collections;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.verifyNoInteractions;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class CardifPeruClosingServiceImplTest {

    private static final String P_HEADER = "test";
    private static final String CORRELATION_ID = "correlation-id";
    private static final String REQUEST_ID = "request-id";

    @Mock
    private CardifPeruClosingRepository repository;

    @Mock
    private CardifPeruClosingExcelHelper excelHelper;

    @InjectMocks
    private CardifPeruClosingServiceImpl service;

    @Nested
    @DisplayName("Generate accounting entries")
    class GenerateAccountingEntries {

        @Test
        @DisplayName("Should execute procedure and return success when pending exist")
        void shouldExecuteProcedureWhenPendingExist() {
            when(repository.countPendingMovements()).thenReturn(2L);

            String result = service.generateAccountingEntries(
                    P_HEADER, CORRELATION_ID, REQUEST_ID);

            assertEquals("Asientos generados con éxito.", result);
            verify(repository).countPendingMovements();
            verify(repository).executeAccountingProcedure();
        }

        @Test
        @DisplayName("Should not execute procedure when there are no pending")
        void shouldNotExecuteProcedureWhenNoPending() {
            when(repository.countPendingMovements()).thenReturn(0L);

            String result = service.generateAccountingEntries(
                    P_HEADER, CORRELATION_ID, REQUEST_ID);

            assertEquals("No hay movimientos para contabilizar.", result);
            verify(repository).countPendingMovements();
            verify(repository, never()).executeAccountingProcedure();
        }

        @Test
        @DisplayName("Should throw BusinessException when counting fails")
        void shouldThrowWhenCountingFails() {
            when(repository.countPendingMovements())
                    .thenThrow(new DataAccessResourceFailureException("DB error"));

            assertThrows(
                    BusinessException.class,
                    () -> service.generateAccountingEntries(
                            P_HEADER, CORRELATION_ID, REQUEST_ID));

            verify(repository, never()).executeAccountingProcedure();
        }

        @Test
        @DisplayName("Should throw BusinessException when procedure fails")
        void shouldThrowWhenProcedureFails() {
            when(repository.countPendingMovements()).thenReturn(1L);
            org.mockito.Mockito.doThrow(
                            new DataAccessResourceFailureException("SP error"))
                    .when(repository).executeAccountingProcedure();

            assertThrows(
                    BusinessException.class,
                    () -> service.generateAccountingEntries(
                            P_HEADER, CORRELATION_ID, REQUEST_ID));

            verify(repository).executeAccountingProcedure();
        }
    }

    @Nested
    @DisplayName("Download movements report")
    class DownloadMovementsReport {

        @Test
        @DisplayName("Should generate Excel successfully")
        void shouldGenerateExcelSuccessfully() throws IOException {
            List<CardifPeruClosing> movements =
                    Collections.singletonList(
                            CardifPeruClosing.builder().build());
            byte[] expectedFile = new byte[]{1, 2, 3};

            when(repository.findAllForExport()).thenReturn(movements);
            when(excelHelper.generateExcel(movements)).thenReturn(expectedFile);

            byte[] result = service.downloadMovementsReport(
                    P_HEADER, CORRELATION_ID, REQUEST_ID);

            assertArrayEquals(expectedFile, result);
            verify(repository).findAllForExport();
            verify(excelHelper).generateExcel(movements);
        }

        @Test
        @DisplayName("Should throw BusinessException when movement list is empty")
        void shouldThrowWhenListIsEmpty() {
            when(repository.findAllForExport())
                    .thenReturn(Collections.emptyList());

            assertThrows(
                    BusinessException.class,
                    () -> service.downloadMovementsReport(
                            P_HEADER, CORRELATION_ID, REQUEST_ID));

            verify(repository).findAllForExport();
            verifyNoInteractions(excelHelper);
        }

        @Test
        @DisplayName("Should throw BusinessException when movement list is null")
        void shouldThrowWhenListIsNull() {
            when(repository.findAllForExport()).thenReturn(null);

            assertThrows(
                    BusinessException.class,
                    () -> service.downloadMovementsReport(
                            P_HEADER, CORRELATION_ID, REQUEST_ID));

            verify(repository).findAllForExport();
            verifyNoInteractions(excelHelper);
        }

        @Test
        @DisplayName("Should throw BusinessException when query fails")
        void shouldThrowWhenQueryFails() {
            when(repository.findAllForExport())
                    .thenThrow(new DataAccessResourceFailureException("DB error"));

            assertThrows(
                    BusinessException.class,
                    () -> service.downloadMovementsReport(
                            P_HEADER, CORRELATION_ID, REQUEST_ID));

            verify(repository).findAllForExport();
            verifyNoInteractions(excelHelper);
        }

        @Test
        @DisplayName("Should throw BusinessException when Excel generation fails")
        void shouldThrowWhenExcelGenerationFails() throws IOException {
            List<CardifPeruClosing> movements =
                    Collections.singletonList(
                            CardifPeruClosing.builder().build());

            when(repository.findAllForExport()).thenReturn(movements);
            when(excelHelper.generateExcel(movements))
                    .thenThrow(new IOException("Excel error"));

            assertThrows(
                    BusinessException.class,
                    () -> service.downloadMovementsReport(
                            P_HEADER, CORRELATION_ID, REQUEST_ID));

            verify(excelHelper).generateExcel(movements);
        }
    }
}
