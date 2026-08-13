package co.com.bnpparibas.cardif.closingclaims.domain.services.impl;

import co.com.bnpparibas.cardif.closingclaims.domain.dtos.loadmovements.ErrorsMovements;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.loadmovements.LoadMovements;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.loadmovements.SearchErrorsMovementsPageDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.entity.*;
import co.com.bnpparibas.cardif.closingclaims.domain.util.anums.StatusFileLoad;
import co.com.bnpparibas.cardif.closingclaims.domain.util.constants.FlagCode;
import co.com.bnpparibas.cardif.closingclaims.domain.util.exception.BusinessException;
import co.com.bnpparibas.cardif.closingclaims.infraestructure.repository.*;
import org.junit.jupiter.api.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.*;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.data.domain.*;
import org.springframework.http.HttpStatus;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.web.multipart.MultipartFile;

import java.io.*;
import java.time.LocalDateTime;
import java.util.*;
import java.util.stream.Stream;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class LoadMovementsCantralAmericaServiceImplTest {

    @Mock private FileUploadTBLRepository fileUploadRepository;
    @Mock private ReadExcelFileTmpOnbaseService readExcelFile;
    @Mock private TBLTmpOnbaseRepository tmpOnbaseRepository;
    @Mock private TBLTmpValidaCargueOnbaseRepository tmpValidaCargueOnbaseRepository;
    @Mock private LogsApplicationRepository logsApplicationRepository;

    @InjectMocks
    private LoadMovementsCantralAmericaServiceImpl service;

    private static final String FLAG_CA = FlagCode.CA;   // “502”
    private static final String MODULE_CODE = "centro_america";
    private static final Integer MODULE_ID = 1;

    /* ----------------------------------------------------------------- *
     *  Helpers
     * ----------------------------------------------------------------- */
    private MultipartFile buildExcelFile(String name) {
        return new MockMultipartFile(
                "file", name,
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                "dummy".getBytes());
    }

    private ArchivoCargueTBL buildArchivoCargue(String fileName) {
        return ArchivoCargueTBL.builder()
                .id(FileLoadId.builder()
                        .nombre(fileName)
                        .fechaproceso(new Date())
                        .build())
                .estado(StatusFileLoad.PENDIENTE.name())
                .errores(1)
                .cargadosanterior(2)
                .porcargar(3)
                .registros(4)
                .idModulo(MODULE_ID)
                .build();
    }

    /* ----------------------------------------------------------------- *
     *  uploadMovements
     * ----------------------------------------------------------------- */
    @Nested
    @DisplayName("uploadMovements")
    class UploadMovements {

        @Test
        @DisplayName("happy path – normal flow")
        void uploadMovements_success() throws Exception {
            MultipartFile file = buildExcelFile("movements.xlsx");

            when(fileUploadRepository.findModuleIdByCode(MODULE_CODE)).thenReturn(MODULE_ID);
            when(fileUploadRepository.getFilePending(MODULE_ID)).thenReturn(0);
            doNothing().when(tmpValidaCargueOnbaseRepository).truncateTable();
            doNothing().when(readExcelFile).processExcel(file, FLAG_CA);
            doNothing().when(fileUploadRepository).executeMovementValidation(MODULE_CODE);
            when(fileUploadRepository.countValidationErrors(MODULE_ID)).thenReturn(0);

            String result = service.uploadMovements("h", "c", "r", file, "userX", FLAG_CA);

            assertEquals("Cargado...", result);
            verify(tmpValidaCargueOnbaseRepository).truncateTable();
            verify(fileUploadRepository).save(argThat(ac ->
                    ac.getId().getNombre().equals("movements.xlsx")
                            && ac.getEstado().equals(StatusFileLoad.PENDIENTE.name())
                            && MODULE_ID.equals(ac.getIdModulo())));
            verify(readExcelFile).processExcel(file, FLAG_CA);
            verify(fileUploadRepository).executeMovementValidation(MODULE_CODE);
            verify(logsApplicationRepository).save(any());
        }

        @Test
        @DisplayName("fails when file is null")
        void uploadMovements_nullFile() {
            BusinessException ex = assertThrows(BusinessException.class,
                    () -> service.uploadMovements("h", "c", "r", null, "user", FLAG_CA));
            assertEquals(HttpStatus.BAD_REQUEST, ex.getHttpStatus());
            assertTrue(ex.getMessage().contains("El archivo es requerido"));
        }

        @Test
        @DisplayName("fails when extension is not xls/xlsx")
        void uploadMovements_invalidExtension() {
            MultipartFile file = new MockMultipartFile("file", "bad.txt", "text/plain", "data".getBytes());

            BusinessException ex = assertThrows(BusinessException.class,
                    () -> service.uploadMovements("h", "c", "r", file, "user", FLAG_CA));
            assertEquals(HttpStatus.UNSUPPORTED_MEDIA_TYPE, ex.getHttpStatus());
            assertTrue(ex.getMessage().contains("Archivo Valido"));
        }

        @Test
        @DisplayName("fails when module is not configured")
        void uploadMovements_moduleNotConfigured() {
            MultipartFile file = buildExcelFile("movements.xlsx");
            when(fileUploadRepository.findModuleIdByCode(MODULE_CODE)).thenReturn(null);

            BusinessException ex = assertThrows(BusinessException.class,
                    () -> service.uploadMovements("h", "c", "r", file, "user", FLAG_CA));

            assertEquals(HttpStatus.PRECONDITION_FAILED, ex.getHttpStatus());
            assertTrue(ex.getMessage().contains("Modulo no configurado"));
            verify(fileUploadRepository, never()).save(any());
        }

        @Test
        @DisplayName("fails when a pending file already exists")
        void uploadMovements_pendingFileExists() {
            MultipartFile file = buildExcelFile("movements.xlsx");
            when(fileUploadRepository.findModuleIdByCode(MODULE_CODE)).thenReturn(MODULE_ID);
            when(fileUploadRepository.getFilePending(MODULE_ID)).thenReturn(5); // >0

            BusinessException ex = assertThrows(BusinessException.class,
                    () -> service.uploadMovements("h", "c", "r", file, "user", FLAG_CA));

            assertEquals(HttpStatus.PRECONDITION_FAILED, ex.getHttpStatus());
            assertTrue(ex.getMessage().contains("Debe primero gestionar el archivo pendiente"));
            verify(fileUploadRepository, never()).save(any());
        }

        @Test
        @DisplayName("removes the pending record when validation reports errors")
        void uploadMovements_validationErrors() {
            MultipartFile file = buildExcelFile("movements.xlsx");

            when(fileUploadRepository.findModuleIdByCode(MODULE_CODE)).thenReturn(MODULE_ID);
            when(fileUploadRepository.getFilePending(MODULE_ID)).thenReturn(0);
            doNothing().when(tmpValidaCargueOnbaseRepository).truncateTable();
            doNothing().when(readExcelFile).processExcel(file, FLAG_CA);
            doNothing().when(fileUploadRepository).executeMovementValidation(MODULE_CODE);
            when(fileUploadRepository.countValidationErrors(MODULE_ID)).thenReturn(3);

            BusinessException ex = assertThrows(BusinessException.class,
                    () -> service.uploadMovements("h", "c", "r", file, "user", FLAG_CA));

            assertEquals(HttpStatus.PRECONDITION_FAILED, ex.getHttpStatus());
            assertTrue(ex.getMessage().contains("Error validando el archivo cargado"));
            verify(fileUploadRepository).deleteLastPending(MODULE_ID);
            verify(logsApplicationRepository, never()).save(any());
        }
    }

    /* ----------------------------------------------------------------- *
     *  extractFileName
     * ----------------------------------------------------------------- */
    @Nested
    @DisplayName("extractFileName")
    class ExtractFileName {

        @Test
        @DisplayName("returns original filename")
        void returnsName() {
            MultipartFile file = buildExcelFile("myfile.xlsx");
            assertEquals("myfile.xlsx", service.extractFileName(file));
        }

        @Test
        @DisplayName("throws when original filename is null")
        void nullName() {
            MultipartFile file = mock(MultipartFile.class);
            when(file.getOriginalFilename()).thenReturn(null);

            BusinessException ex = assertThrows(BusinessException.class,
                    () -> service.extractFileName(file));
            assertEquals(HttpStatus.BAD_REQUEST, ex.getHttpStatus());
            assertTrue(ex.getMessage().contains("no puede ser nulo o vacío"));
        }

        @Test
        @DisplayName("throws when original filename is blank")
        void blankName() {
            MultipartFile file = mock(MultipartFile.class);
            when(file.getOriginalFilename()).thenReturn("   ");

            BusinessException ex = assertThrows(BusinessException.class,
                    () -> service.extractFileName(file));
            assertEquals(HttpStatus.BAD_REQUEST, ex.getHttpStatus());
        }
    }

    /* ----------------------------------------------------------------- *
     *  getPendingUploads
     * ----------------------------------------------------------------- */
    @Test
    @DisplayName("getPendingUploads maps entities to DTO")
    void getPendingUploads_maps() {
        ArchivoCargueTBL entity = buildArchivoCargue("file1.xlsx");
        when(fileUploadRepository.findModuleIdByCode(MODULE_CODE)).thenReturn(MODULE_ID);
        when(fileUploadRepository.findByEstadoAndModule(StatusFileLoad.PENDIENTE.name(), MODULE_ID))
                .thenReturn(Collections.singletonList(entity));

        List<LoadMovements> result = service.getPendingUploads("h", "c", "r", FLAG_CA);

        assertEquals(1, result.size());
        LoadMovements dto = result.get(0);
        assertEquals("file1.xlsx", dto.getFile());
        assertEquals(1, dto.getNumberErrors());
        assertEquals(2, dto.getNumberRecordsAlreadyLoaded());
        assertEquals(3, dto.getRecordsNumberUpload());
        assertEquals(4, dto.getTotalRecords());
        assertNotNull(dto.getDateProcess());
    }

    @Test
    @DisplayName("getPendingUploads fails when module is not configured")
    void getPendingUploads_moduleNotConfigured() {
        when(fileUploadRepository.findModuleIdByCode(MODULE_CODE)).thenReturn(null);

        BusinessException ex = assertThrows(BusinessException.class,
                () -> service.getPendingUploads("h", "c", "r", FLAG_CA));

        assertEquals(HttpStatus.PRECONDITION_FAILED, ex.getHttpStatus());
        assertTrue(ex.getMessage().contains("Modulo no configurado"));
    }

    /* ----------------------------------------------------------------- *
     *  getErrorsMovements
     * ----------------------------------------------------------------- */
    @Test
    @DisplayName("getErrorsMovements returns paged DTO")
    void getErrorsMovements_returnsPageDto() {
        TBLTmpValidaCargueOnbase tmp = TBLTmpValidaCargueOnbase.builder()
                .id(TmpOnbaseId.builder().idMovimiento("M123").numerDeSiniestro("S456").build())
                .desError("Error de prueba")
                .build();

        Page<TBLTmpValidaCargueOnbase> page = mock(Page.class);
        when(page.stream()).thenReturn(Stream.of(tmp));
        when(page.getNumber()).thenReturn(0);
        when(page.getTotalPages()).thenReturn(2);
        when(page.getTotalElements()).thenReturn(1L);

        when(tmpValidaCargueOnbaseRepository.findByError(eq(1), any()))
                .thenReturn(page);

        SearchErrorsMovementsPageDTO result = service.getErrorsMovements("h", "c", "r", 0, 10, FLAG_CA);

        assertNotNull(result);
        assertEquals(1, result.getErrorsMovements().size());
        ErrorsMovements em = result.getErrorsMovements().get(0);
        assertEquals("M123", em.getIdMovement());
        assertEquals("Error de prueba", em.getDesError());

        assertEquals(0, result.getCurrentPage());
        assertEquals(2, result.getTotalPages());
        assertEquals(1, result.getRemainingPages()); // 2 - 0 - 1
        assertEquals(1L, result.getTotalElements());
    }

    /* ----------------------------------------------------------------- *
     *  deleteMovementLoad
     * ----------------------------------------------------------------- */
    @Nested
    @DisplayName("deleteMovementLoad")
    class DeleteMovementLoad {

        private final String fileName = "toDelete.xlsx";

        @Test
        @DisplayName("successful deletion")
        void delete_successful() {
            when(fileUploadRepository.findModuleIdByCode(MODULE_CODE)).thenReturn(MODULE_ID);
            when(fileUploadRepository.markAsDeletedByFileName(fileName, MODULE_ID)).thenReturn(1);
            doNothing().when(tmpOnbaseRepository).deleteAll();
            doNothing().when(tmpValidaCargueOnbaseRepository).deleteAll();

            assertDoesNotThrow(() -> service.deleteMovementLoad("h", "c", "r", fileName, FLAG_CA));

            verify(fileUploadRepository).markAsDeletedByFileName(fileName, MODULE_ID);
            verify(tmpOnbaseRepository).deleteAll();
            verify(tmpValidaCargueOnbaseRepository).deleteAll();
        }

        @Test
        @DisplayName("throws NOT_FOUND when no rows updated")
        void delete_notFound() {
            when(fileUploadRepository.findModuleIdByCode(MODULE_CODE)).thenReturn(MODULE_ID);
            when(fileUploadRepository.markAsDeletedByFileName(fileName, MODULE_ID)).thenReturn(0);

            BusinessException ex = assertThrows(BusinessException.class,
                    () -> service.deleteMovementLoad("h", "c", "r", fileName, FLAG_CA));

            assertEquals(HttpStatus.NOT_FOUND, ex.getHttpStatus());
            assertTrue(ex.getMessage().contains("No se encontró"));
        }

        @Test
        @DisplayName("throws PRECONDITION_FAILED when module is not configured")
        void delete_moduleNotConfigured() {
            when(fileUploadRepository.findModuleIdByCode(MODULE_CODE)).thenReturn(null);

            BusinessException ex = assertThrows(BusinessException.class,
                    () -> service.deleteMovementLoad("h", "c", "r", fileName, FLAG_CA));

            assertEquals(HttpStatus.PRECONDITION_FAILED, ex.getHttpStatus());
            assertTrue(ex.getMessage().contains("Modulo no configurado"));
        }

        @Test
        @DisplayName("fails when fileName is blank")
        void delete_blankFileName() {
            BusinessException ex = assertThrows(BusinessException.class,
                    () -> service.deleteMovementLoad("h", "c", "r", "   ", FLAG_CA));
            assertEquals(HttpStatus.BAD_REQUEST, ex.getHttpStatus());
            assertTrue(ex.getMessage().contains("nombre del archivo es requerido"));
        }

        @Test
        @DisplayName("wraps unexpected exception in BusinessException")
        void delete_unexpectedException() {
            when(fileUploadRepository.findModuleIdByCode(MODULE_CODE)).thenReturn(MODULE_ID);
            when(fileUploadRepository.markAsDeletedByFileName(fileName, MODULE_ID)).thenReturn(1);
            doThrow(new RuntimeException("DB error")).when(tmpOnbaseRepository).deleteAll();

            BusinessException ex = assertThrows(BusinessException.class,
                    () -> service.deleteMovementLoad("h", "c", "r", fileName, FLAG_CA));

            assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, ex.getHttpStatus());
            assertTrue(ex.getMessage().contains("Error en la Ejecucion"));
        }
    }

    /* ----------------------------------------------------------------- *
     *  insertMovements
     * ----------------------------------------------------------------- */
    @Nested
    @DisplayName("insertMovements")
    class InsertMovements {

        @Test
        @DisplayName("forwards call to repository")
        void insert_successful() {
            String file = "file.xlsx";
            doNothing().when(fileUploadRepository).insertMovements(file, MODULE_CODE);

            assertDoesNotThrow(() -> service.insertMovements("h", "c", "r", file, FLAG_CA));

            verify(fileUploadRepository).insertMovements(file, MODULE_CODE);
        }

        @Test
        @DisplayName("validates fileName")
        void insert_invalidFileName() {
            BusinessException ex = assertThrows(BusinessException.class,
                    () -> service.insertMovements("h", "c", "r", " ", FLAG_CA));
            assertEquals(HttpStatus.BAD_REQUEST, ex.getHttpStatus());
        }

        @Test
        @DisplayName("wraps repository exception")
        void insert_repositoryThrows() {
            String file = "file.xlsx";
            doThrow(new RuntimeException("DB error")).when(fileUploadRepository).insertMovements(file, MODULE_CODE);

            BusinessException ex = assertThrows(BusinessException.class,
                    () -> service.insertMovements("h", "c", "r", file, FLAG_CA));

            assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, ex.getHttpStatus());
            assertTrue(ex.getMessage().contains("Error en la Ejecucion"));
        }
    }

    /* ----------------------------------------------------------------- *
     *  saveLogApplication – error path
     * ----------------------------------------------------------------- */
    @Test
    @DisplayName("saveLogApplication wraps repository exception")
    void saveLogApplication_repositoryThrows() {
        doThrow(new RuntimeException("DB error"))
                .when(logsApplicationRepository).save(any());

        BusinessException ex = assertThrows(BusinessException.class,
                () -> service.saveLogApplication("anyUser"));

        assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, ex.getHttpStatus());
        assertTrue(ex.getMessage().contains("persistiendo log"));
    }
}
