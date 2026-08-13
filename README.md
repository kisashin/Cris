package co.com.bnpparibas.cardif.closingclaims.domain.services.impl;

import co.com.bnpparibas.cardif.closingclaims.domain.dtos.loadmovements.ErrorsMovements;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.loadmovements.LoadMovements;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.loadmovements.SearchErrorsMovementsPageDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.entity.*;
import co.com.bnpparibas.cardif.closingclaims.domain.services.ILoadMovementsCentralAmericaService;
import co.com.bnpparibas.cardif.closingclaims.domain.util.anums.StatusFileLoad;
import co.com.bnpparibas.cardif.closingclaims.domain.util.exception.BusinessException;
import co.com.bnpparibas.cardif.closingclaims.infraestructure.repository.*;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.multipart.MultipartFile;

import java.time.LocalDateTime;
import java.util.Date;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class LoadMovementsCantralAmericaServiceImpl implements ILoadMovementsCentralAmericaService {

    private static final String MODULE_CODE = "centro_america";

    private final FileUploadTBLRepository fileUploadRepository;
    private final ReadExcelFileTmpOnbaseService readExcelFile;
    private final TBLTmpOnbaseRepository tmpOnbaseRepository;
    private final TBLTmpValidaCargueOnbaseRepository tmpValidaCargueOnbaseRepository;
    private final LogsApplicationRepository logsApplicationRepository;

    public LoadMovementsCantralAmericaServiceImpl(FileUploadTBLRepository fileUploadRepository, ReadExcelFileTmpOnbaseService readExcelFile, TBLTmpOnbaseRepository tmpOnbaseRepository, TBLTmpValidaCargueOnbaseRepository tmpValidaCargueOnbaseRepository, LogsApplicationRepository logsApplicationRepository) {
        this.fileUploadRepository = fileUploadRepository;
        this.readExcelFile = readExcelFile;
        this.tmpOnbaseRepository = tmpOnbaseRepository;
        this.tmpValidaCargueOnbaseRepository = tmpValidaCargueOnbaseRepository;
        this.logsApplicationRepository = logsApplicationRepository;
    }

    /**
     * Metodo encargado de caargar los movimientos
     *
     * @param pHeader
     * @param correlationId
     * @param requestId
     * @param file
     * @return
     */
    @Override
    public String uploadMovements(String pHeader, String correlationId, String requestId, MultipartFile file, String user, String flagCountry) {
        // Validar que el archivo no sea nulo y tenga extensión .xlsx o .xls
        if (file == null || file.isEmpty()) {
            throw new BusinessException(null, "El archivo es requerido y no puede estar vacío.", HttpStatus.BAD_REQUEST);
        }

        String filename = extractFileName(file);
        if (!(filename.endsWith(".xlsx") || filename.endsWith(".xls"))) {
            throw new BusinessException(null, "Error: Debe Seleccionar un Archivo Valido (.xlsx o .xls).", HttpStatus.UNSUPPORTED_MEDIA_TYPE);
        }

        Integer moduleId = fileUploadRepository.findModuleIdByCode(MODULE_CODE);
        if (moduleId == null) {
            throw new BusinessException(null, "Error: Modulo no configurado.", HttpStatus.PRECONDITION_FAILED);
        }

        // Se valida que no existan archivos en estado pendiente
        int fileStatusPending = fileUploadRepository.getFilePending(moduleId);
        if(fileStatusPending != 0){
            throw new BusinessException(null, "Error: Debe primero gestionar el archivo pendiente.", HttpStatus.PRECONDITION_FAILED);
        }

        tmpValidaCargueOnbaseRepository.truncateTable();

        // Se crea el registro de carga con los datos del archivo
        savePendingLoadFile(filename, moduleId);

        // insertar los registro en la tabla dbo.tmpOnbase
        readExcelFile.processExcel(file, flagCountry);

        //Valida movimientos SP
        fileUploadRepository.executeMovementValidation(MODULE_CODE);

        if (fileUploadRepository.countValidationErrors(moduleId) > 0) {
            fileUploadRepository.deleteLastPending(moduleId);
            throw new BusinessException(null, "Error validando el archivo cargado.", HttpStatus.PRECONDITION_FAILED);
        }

        //insert logs
        saveLogApplication(user);

        return "Cargado...";
    }

    @Transactional
    public void saveLogApplication(String user) {
        String userValue = null;
        if (user != null && !user.isEmpty()) {
            userValue = user.length() > 100 ? user.substring(0, 100) : user;
        }
        try {
            logsApplicationRepository.save(LogsApplication.builder()
                    .application("Siniestros")
                    .nameProcess("Cargar")
                    .process("Cargue Movimientos CA")
                    .accion("BtnCargar")
                    .script("N/A")
                    .dateSystem(LocalDateTime.now())
                    .user(userValue)
                    .build());
        } catch (Exception e ){
            throw new BusinessException(e, null, "Error: persistiendo log.", HttpStatus.INTERNAL_SERVER_ERROR);
        }

    }

    @Transactional
    public void savePendingLoadFile(String filename, Integer moduleId) {
        fileUploadRepository.save(ArchivoCargueTBL.builder()
                .estado(StatusFileLoad.PENDIENTE.name())
                .idModulo(moduleId)
                .id(FileLoadId.builder().nombre(filename).fechaproceso(new Date()).build())
                .build());
    }

    /**
     * Obtiene el nombre original del archivo recibido.
     *
     * @param file archivo multipart
     * @return nombre del archivo
     */
    public String extractFileName(MultipartFile file) {
        String filename = file.getOriginalFilename();
        if (filename == null || filename.trim().isEmpty()) {
            throw new BusinessException(null, "El nombre del archivo no puede ser nulo o vacío.", HttpStatus.BAD_REQUEST);
        }
        return filename;
    }

    /**
     * Metodo encargado de obtener los movimientos en estado 'PENDIENTE'
     *
     * @param pHeader
     * @param correlationId
     * @param requestId
     * @return retorna la lista de movimientos
     */
    @Override
    @Transactional(readOnly = true)
    public List<LoadMovements> getPendingUploads(String pHeader, String correlationId, String requestId, String flagCountry) {
        Integer moduleId = fileUploadRepository.findModuleIdByCode(MODULE_CODE);
        if (moduleId == null) {
            throw new BusinessException(null, "Error: Modulo no configurado.", HttpStatus.PRECONDITION_FAILED);
        }
        List<ArchivoCargueTBL> pendingUploads = fileUploadRepository.findByEstadoAndModule(StatusFileLoad.PENDIENTE.name(), moduleId);
        return pendingUploads.stream().map(p -> LoadMovements
                .builder()
                .dateProcess(p.getId().getFechaproceso())
                .numberErrors(p.getErrores())
                .numberRecordsAlreadyLoaded(p.getCargadosanterior())
                .recordsNumberUpload(p.getPorcargar())
                .totalRecords(p.getRegistros())
                .file(p.getId().getNombre())
                .build()).collect(Collectors.toList());
    }

    @Override
    public SearchErrorsMovementsPageDTO getErrorsMovements(String pHeader, String correlationId, String requestId, Integer page, Integer pageSize, String flagCountry) {
        int pageNumber = (page == null) ? 0 : page;
        int size = (pageSize == null) ? 50 : pageSize;
        Pageable pageable = PageRequest.of(pageNumber, size);
        Page<TBLTmpValidaCargueOnbase> result = tmpValidaCargueOnbaseRepository.findByError(1, pageable);
        List<ErrorsMovements> errorsMovementsList = result.stream()
                .map(r -> ErrorsMovements
                        .builder()
                        .idMovement(r.getId().getIdMovimiento())
                        .desError(r.getDesError())
                        .build()).collect(Collectors.toList());
        return SearchErrorsMovementsPageDTO.builder()
                .errorsMovements(errorsMovementsList)
                .currentPage(result.getNumber())
                .totalPages(result.getTotalPages())
                .remainingPages(result.getTotalPages() - result.getNumber() - 1)
                .totalElements(result.getTotalElements())
                .build();
    }

    @Override
    @Transactional
    public void deleteMovementLoad(String pHeader, String correlationId, String requestId, String fileName, String flagCountry) {
        // Validar nombre del archivo
        if (fileName == null || fileName.trim().isEmpty()) {
            throw new BusinessException(null,
                    "El nombre del archivo es requerido y no puede estar vacío.",
                    HttpStatus.BAD_REQUEST);
        }

        try {
            Integer moduleId = fileUploadRepository.findModuleIdByCode(MODULE_CODE);
            if (moduleId == null) {
                throw new BusinessException(null,
                        "Error: Modulo no configurado.",
                        HttpStatus.PRECONDITION_FAILED);
            }

            // Actualiza los registros por nombre a estado: DELETE
            int rowsUpdated = fileUploadRepository.markAsDeletedByFileName(fileName, moduleId);
            if (rowsUpdated == 0) {
                throw new BusinessException(null,
                        "No se encontró ningún registro para el archivo: " + fileName,
                        HttpStatus.NOT_FOUND);
            }
            // Elimina los registros temporales en las tablas tmponbase
            tmpOnbaseRepository.deleteAll();
            tmpValidaCargueOnbaseRepository.deleteAll();

        } catch (BusinessException be) {
            // Propagar excepciones de negocio sin modificar
            throw be;
        } catch (Exception ex) {
            // Capturar cualquier otro error y envolverlo en BusinessException
            throw new BusinessException(ex, null,
                    "Error en la Ejecucion al intentar eliminar la carga de movimientos.",
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    @Transactional
    public void insertMovements(String pHeader, String correlationId, String requestId, String fileName, String flagCountry) {
        // Validar nombre del archivo
        if (fileName == null || fileName.trim().isEmpty()) {
            throw new BusinessException(null,
                    "El nombre del archivo es requerido y no puede estar vacío.",
                    HttpStatus.BAD_REQUEST);
        }

        try {
            fileUploadRepository.insertMovements(fileName, MODULE_CODE);
        } catch (Exception ex) {
            throw new BusinessException(ex, null,
                    "Error en la Ejecucion: " + fileName,
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }
}
