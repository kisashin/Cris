package co.com.bnpparibas.cardif.closingclaims.domain.services.impl;

import co.com.bnpparibas.cardif.closingclaims.domain.dtos.cardifcenterclosing.AccountingXmlFileDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.cardifcenterclosing.AccountingXmlLine;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.cardifcenterclosing.CenterAccountingResultDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.entity.CardifCenterClosing;
import co.com.bnpparibas.cardif.closingclaims.domain.util.exception.BusinessException;
import co.com.bnpparibas.cardif.closingclaims.domain.util.helpers.CardifCenterAccountingXmlHelper;
import co.com.bnpparibas.cardif.closingclaims.domain.util.helpers.CardifCenterClosingExcelHelper;
import co.com.bnpparibas.cardif.closingclaims.infraestructure.repository.CardifCenterClosingRepository;
import co.com.bnpparibas.cardif.closingclaims.infraestructure.repository.StoredProcedureExecutor;
import co.com.bnpparibas.cardif.closingclaims.infraestructure.repository.StoredProcedureRowMapper;
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
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.verifyNoInteractions;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class CardifCenterClosingServiceImplTest {

    private static final String P_HEADER = "test";
    private static final String CORRELATION_ID = "correlation-id";
    private static final String REQUEST_ID = "request-id";

    @Mock
    private CardifCenterClosingRepository repository;

    @Mock
    private CardifCenterClosingExcelHelper excelHelper;

    @Mock
    private CardifCenterAccountingXmlHelper xmlHelper;

    @Mock
    private StoredProcedureExecutor storedProcedureExecutor;

    @InjectMocks
    private CardifCenterClosingServiceImpl service;

    @Nested
    @DisplayName("Generate accounting entries")
    class GenerateAccountingEntries {

        @Test
        @DisplayName("Should return generated files when pending exist")
        void shouldReturnGeneratedFilesWhenPendingExist() {
            List<AccountingXmlLine> lines = Collections.singletonList(
                    AccountingXmlLine.builder()
                            .period("202608")
                            .pass(1)
                            .lineType(2)
                            .movementType("Pago")
                            .sequence(1L)
                            .content("<Line>PAGO-1</Line>")
                            .build());

            List<AccountingXmlFileDTO> files = Collections.singletonList(
                    AccountingXmlFileDTO.builder()
                            .movementType("Pago")
                            .fileName("Sinie_ReasegCentro_Pago20260824.xml")
                            .lineCount(1)
                            .content("Y29udGVudA==")
                            .build());

            when(repository.countPendingMovements()).thenReturn(2L);
            when(storedProcedureExecutor.query(
                    anyString(), any(StoredProcedureRowMapper.class)))
                    .thenReturn(lines);
            when(xmlHelper.buildFiles(lines)).thenReturn(files);

            CenterAccountingResultDTO result =
                    service.generateAccountingEntries(
                            P_HEADER, CORRELATION_ID, REQUEST_ID);

            assertEquals("Asientos generados con éxito.", result.getMessage());
            assertEquals("PROCESADO", result.getStatus());
            assertEquals("202608", result.getPeriod());
            assertEquals(1, result.getFiles().size());
            assertNotNull(result.getProcessDate());

            verify(repository).countPendingMovements();
            verify(xmlHelper).buildFiles(lines);
        }

        @Test
        @DisplayName("Should not execute procedure when there are no pending")
        void shouldNotExecuteProcedureWhenNoPending() {
            when(repository.countPendingMovements()).thenReturn(0L);

            CenterAccountingResultDTO result =
                    service.generateAccountingEntries(
                            P_HEADER, CORRELATION_ID, REQUEST_ID);

            assertEquals(
                    "No hay movimientos para contabilizar.",
                    result.getMessage());
            assertEquals("SIN MOVIMIENTOS", result.getStatus());
            assertTrue(result.getFiles().isEmpty());

            verifyNoInteractions(storedProcedureExecutor);
            verifyNoInteractions(xmlHelper);
        }

        @Test
        @DisplayName("Should throw BusinessException when no files are built")
        void shouldThrowWhenNoFilesAreBuilt() {
            when(repository.countPendingMovements()).thenReturn(5L);
            when(storedProcedureExecutor.query(
                    anyString(), any(StoredProcedureRowMapper.class)))
                    .thenReturn(Collections.emptyList());
            when(xmlHelper.buildFiles(Collections.emptyList()))
                    .thenReturn(Collections.emptyList());

            assertThrows(
                    BusinessException.class,
                    () -> service.generateAccountingEntries(
                            P_HEADER, CORRELATION_ID, REQUEST_ID));
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

            verifyNoInteractions(storedProcedureExecutor);
        }

        @Test
        @DisplayName("Should throw BusinessException when procedure fails")
        void shouldThrowWhenProcedureFails() {
            when(repository.countPendingMovements()).thenReturn(1L);
            when(storedProcedureExecutor.query(
                    anyString(), any(StoredProcedureRowMapper.class)))
                    .thenThrow(new DataAccessResourceFailureException("SP error"));

            assertThrows(
                    BusinessException.class,
                    () -> service.generateAccountingEntries(
                            P_HEADER, CORRELATION_ID, REQUEST_ID));

            verifyNoInteractions(xmlHelper);
        }

        @Test
        @DisplayName("Should throw BusinessException when XML building fails")
        void shouldThrowWhenXmlBuildingFails() {
            List<AccountingXmlLine> lines = Collections.singletonList(
                    AccountingXmlLine.builder().lineType(2).build());

            when(repository.countPendingMovements()).thenReturn(1L);
            when(storedProcedureExecutor.query(
                    anyString(), any(StoredProcedureRowMapper.class)))
                    .thenReturn(lines);
            when(xmlHelper.buildFiles(lines))
                    .thenThrow(new IllegalStateException("XML error"));

            assertThrows(
                    BusinessException.class,
                    () -> service.generateAccountingEntries(
                            P_HEADER, CORRELATION_ID, REQUEST_ID));
        }
    }

    @Nested
    @DisplayName("Download movements report")
    class DownloadMovementsReport {

        @Test
        @DisplayName("Should generate Excel successfully")
        void shouldGenerateExcelSuccessfully() throws IOException {
            List<CardifCenterClosing> movements =
                    Collections.singletonList(
                            CardifCenterClosing.builder().build());
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
            List<CardifCenterClosing> movements =
                    Collections.singletonList(
                            CardifCenterClosing.builder().build());

            when(repository.findAllForExport()).thenReturn(movements);
            when(excelHelper.generateExcel(movements))
                    .thenThrow(new IOException("Excel error"));

            assertThrows(
                    BusinessException.class,
                    () -> service.downloadMovementsReport(
                            P_HEADER, CORRELATION_ID, REQUEST_ID));

            verify(excelHelper).generateExcel(movements);
            verify(repository, never()).countPendingMovements();
        }
    }
}
