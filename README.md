package co.com.bnpparibas.cardif.closingclaims.domain.services.impl;

import co.com.bnpparibas.cardif.closingclaims.domain.dtos.cardifcenterclosing.AccountingXmlFile;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.cardifcenterclosing.AccountingXmlFileDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.cardifcenterclosing.AccountingXmlLine;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.cardifcenterclosing.CenterAccountingResultDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.entity.ArchivoAsientoCentro;
import co.com.bnpparibas.cardif.closingclaims.domain.entity.CardifCenterClosing;
import co.com.bnpparibas.cardif.closingclaims.domain.util.exception.BusinessException;
import co.com.bnpparibas.cardif.closingclaims.domain.util.helpers.CardifCenterAccountingXmlHelper;
import co.com.bnpparibas.cardif.closingclaims.domain.util.helpers.CardifCenterClosingExcelHelper;
import co.com.bnpparibas.cardif.closingclaims.infraestructure.repository.ArchivoAsientoCentroRepository;
import co.com.bnpparibas.cardif.closingclaims.infraestructure.repository.CardifCenterClosingRepository;
import co.com.bnpparibas.cardif.closingclaims.infraestructure.repository.StoredProcedureExecutor;
import co.com.bnpparibas.cardif.closingclaims.infraestructure.repository.StoredProcedureRowMapper;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.InOrder;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.dao.DataAccessResourceFailureException;

import java.io.IOException;
import java.time.LocalDateTime;
import java.util.Collections;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyList;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.inOrder;
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
    private ArchivoAsientoCentroRepository fileRepository;

    @Mock
    private CardifCenterClosingExcelHelper excelHelper;

    @Mock
    private CardifCenterAccountingXmlHelper xmlHelper;

    @Mock
    private StoredProcedureExecutor storedProcedureExecutor;

    @InjectMocks
    private CardifCenterClosingServiceImpl service;

    private AccountingXmlLine line() {
        return AccountingXmlLine.builder()
                .period("202608")
                .pass(1)
                .lineType(2)
                .movementType("Pago")
                .sequence(1L)
                .content("<Line>PAGO-1</Line>")
                .build();
    }

    private AccountingXmlFile file() {
        return AccountingXmlFile.builder()
                .movementType("Pago")
                .fileName("Sinie_ReasegCentro_Pago20260824.xml")
                .lineCount(2)
                .content("<SSC/>")
                .build();
    }

    private ArchivoAsientoCentro entity() {
        return ArchivoAsientoCentro.builder()
                .id(1)
                .idLote("lote")
                .periodo("202608")
                .tipoMovimiento("Pago")
                .nombreArchivo("Sinie_ReasegCentro_Pago20260824.xml")
                .contenido("<SSC/>")
                .cantidadLineas(2)
                .fechaproceso(LocalDateTime.of(2026, 8, 24, 15, 3, 29))
                .estado("GENERADO")
                .build();
    }

    @Nested
    @DisplayName("Generate accounting entries")
    class GenerateAccountingEntries {

        @Test
        @DisplayName("Should persist the generated files and return them")
        void shouldPersistGeneratedFiles() {
            List<AccountingXmlLine> lines = Collections.singletonList(line());
            List<AccountingXmlFile> files = Collections.singletonList(file());

            when(storedProcedureExecutor.query(
                    anyString(), any(StoredProcedureRowMapper.class)))
                    .thenReturn(lines);
            when(xmlHelper.buildFiles(lines)).thenReturn(files);
            when(fileRepository.saveAll(anyList()))
                    .thenReturn(Collections.singletonList(entity()));

            CenterAccountingResultDTO result =
                    service.generateAccountingEntries(
                            P_HEADER, CORRELATION_ID, REQUEST_ID);

            assertEquals("Asientos generados con éxito.", result.getMessage());
            assertEquals("202608", result.getPeriod());
            assertEquals(1, result.getFiles().size());
            assertEquals(1, result.getFiles().get(0).getId());
            assertEquals("GENERADO", result.getFiles().get(0).getStatus());
            assertNotNull(result.getFiles().get(0).getProcessDate());

            // NUEVO
            InOrder order = inOrder(fileRepository, storedProcedureExecutor);
            order.verify(fileRepository).deleteAllFiles();
            order.verify(storedProcedureExecutor).query(
                    anyString(), any(StoredProcedureRowMapper.class));
            order.verify(fileRepository).saveAll(anyList());
        }

        // NUEVO
        @Test
        @DisplayName("Should not delete previous files when the delete fails")
        void shouldThrowWhenDeleteFails() {
            when(fileRepository.deleteAllFiles())
                    .thenThrow(new DataAccessResourceFailureException("DB error"));

            assertThrows(
                    BusinessException.class,
                    () -> service.generateAccountingEntries(
                            P_HEADER, CORRELATION_ID, REQUEST_ID));

            verifyNoInteractions(storedProcedureExecutor);
            verifyNoInteractions(xmlHelper);
        }

        @Test
        @DisplayName("Should save every file with the same batch id")
        void shouldSaveEveryFileWithTheSameBatchId() {
            List<AccountingXmlLine> lines = Collections.singletonList(line());
            List<AccountingXmlFile> files = Collections.singletonList(file());

            when(storedProcedureExecutor.query(
                    anyString(), any(StoredProcedureRowMapper.class)))
                    .thenReturn(lines);
            when(xmlHelper.buildFiles(lines)).thenReturn(files);
            when(fileRepository.saveAll(anyList()))
                    .thenReturn(Collections.singletonList(entity()));

            service.generateAccountingEntries(
                    P_HEADER, CORRELATION_ID, REQUEST_ID);

            ArgumentCaptor<List<ArchivoAsientoCentro>> captor =
                    ArgumentCaptor.forClass(List.class);
            verify(fileRepository).saveAll(captor.capture());

            ArchivoAsientoCentro saved = captor.getValue().get(0);

            assertNotNull(saved.getIdLote());
            assertEquals("202608", saved.getPeriodo());
            assertEquals("Pago", saved.getTipoMovimiento());
            assertEquals("<SSC/>", saved.getContenido());
            assertEquals("GENERADO", saved.getEstado());
        }

        @Test
        @DisplayName("Should throw BusinessException when no files are built")
        void shouldThrowWhenNoFilesAreBuilt() {
            when(storedProcedureExecutor.query(
                    anyString(), any(StoredProcedureRowMapper.class)))
                    .thenReturn(Collections.emptyList());
            when(xmlHelper.buildFiles(Collections.emptyList()))
                    .thenReturn(Collections.emptyList());

            assertThrows(
                    BusinessException.class,
                    () -> service.generateAccountingEntries(
                            P_HEADER, CORRELATION_ID, REQUEST_ID));

            verifyNoInteractions(fileRepository);
        }

        @Test
        @DisplayName("Should throw BusinessException when the procedure fails")
        void shouldThrowWhenProcedureFails() {
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
            List<AccountingXmlLine> lines = Collections.singletonList(line());

            when(storedProcedureExecutor.query(
                    anyString(), any(StoredProcedureRowMapper.class)))
                    .thenReturn(lines);
            when(xmlHelper.buildFiles(lines))
                    .thenThrow(new IllegalStateException("XML error"));

            assertThrows(
                    BusinessException.class,
                    () -> service.generateAccountingEntries(
                            P_HEADER, CORRELATION_ID, REQUEST_ID));

            verifyNoInteractions(fileRepository);
        }

        @Test
        @DisplayName("Should throw BusinessException when saving fails")
        void shouldThrowWhenSavingFails() {
            List<AccountingXmlLine> lines = Collections.singletonList(line());
            List<AccountingXmlFile> files = Collections.singletonList(file());

            when(storedProcedureExecutor.query(
                    anyString(), any(StoredProcedureRowMapper.class)))
                    .thenReturn(lines);
            when(xmlHelper.buildFiles(lines)).thenReturn(files);
            when(fileRepository.saveAll(anyList()))
                    .thenThrow(new DataAccessResourceFailureException("DB error"));

            assertThrows(
                    BusinessException.class,
                    () -> service.generateAccountingEntries(
                            P_HEADER, CORRELATION_ID, REQUEST_ID));
        }
    }

    @Nested
    @DisplayName("Find generated files")
    class FindGeneratedFiles {

        @Test
        @DisplayName("Should map the persisted files")
        void shouldMapPersistedFiles() {
            when(fileRepository.findLatest())
                    .thenReturn(Collections.singletonList(entity()));

            List<AccountingXmlFileDTO> files =
                    service.findGeneratedFiles(CORRELATION_ID, REQUEST_ID);

            assertEquals(1, files.size());
            assertEquals("Pago", files.get(0).getMovementType());
            assertEquals(2, files.get(0).getLineCount());
            assertTrue(files.get(0).getProcessDate()
                    .startsWith("24/08/2026 03:03:29"));
        }

        @Test
        @DisplayName("Should return an empty list when there is no history")
        void shouldReturnEmptyListWhenThereIsNoHistory() {
            when(fileRepository.findLatest())
                    .thenReturn(Collections.emptyList());

            assertTrue(service.findGeneratedFiles(
                    CORRELATION_ID, REQUEST_ID).isEmpty());
        }

        @Test
        @DisplayName("Should throw BusinessException when the query fails")
        void shouldThrowWhenQueryFails() {
            when(fileRepository.findLatest())
                    .thenThrow(new DataAccessResourceFailureException("DB error"));

            assertThrows(
                    BusinessException.class,
                    () -> service.findGeneratedFiles(
                            CORRELATION_ID, REQUEST_ID));
        }
    }

    @Nested
    @DisplayName("Find XML file")
    class FindXmlFile {

        @Test
        @DisplayName("Should return the persisted file")
        void shouldReturnPersistedFile() {
            when(fileRepository.findById(1))
                    .thenReturn(Optional.of(entity()));

            ArchivoAsientoCentro file =
                    service.findXmlFile(1, CORRELATION_ID, REQUEST_ID);

            assertEquals("<SSC/>", file.getContenido());
        }

        @Test
        @DisplayName("Should throw BusinessException when the file does not exist")
        void shouldThrowWhenFileDoesNotExist() {
            when(fileRepository.findById(9)).thenReturn(Optional.empty());

            assertThrows(
                    BusinessException.class,
                    () -> service.findXmlFile(9, CORRELATION_ID, REQUEST_ID));
        }

        @Test
        @DisplayName("Should throw BusinessException when the file has no content")
        void shouldThrowWhenFileHasNoContent() {
            ArchivoAsientoCentro empty = entity();
            empty.setContenido(null);

            when(fileRepository.findById(1)).thenReturn(Optional.of(empty));

            assertThrows(
                    BusinessException.class,
                    () -> service.findXmlFile(1, CORRELATION_ID, REQUEST_ID));
        }

        @Test
        @DisplayName("Should throw BusinessException when the query fails")
        void shouldThrowWhenQueryFails() {
            when(fileRepository.findById(1))
                    .thenThrow(new DataAccessResourceFailureException("DB error"));

            assertThrows(
                    BusinessException.class,
                    () -> service.findXmlFile(1, CORRELATION_ID, REQUEST_ID));
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

            verifyNoInteractions(excelHelper);
        }

        @Test
        @DisplayName("Should throw BusinessException when the query fails")
        void shouldThrowWhenQueryFails() {
            when(repository.findAllForExport())
                    .thenThrow(new DataAccessResourceFailureException("DB error"));

            assertThrows(
                    BusinessException.class,
                    () -> service.downloadMovementsReport(
                            P_HEADER, CORRELATION_ID, REQUEST_ID));

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
        }
    }
}
