package co.com.bnpparibas.cardif.closingclaims.infraestructure.repository;

import co.com.bnpparibas.cardif.closingclaims.domain.entity.ArchivoCargueTBL;
import co.com.bnpparibas.cardif.closingclaims.domain.entity.FileLoadId;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.jpa.repository.query.Procedure;
import org.springframework.data.repository.query.Param;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

public interface FileUploadTBLRepository extends JpaRepository<ArchivoCargueTBL, FileLoadId> {

    @Query(value = "SELECT id_modulo FROM dbo.TBL_Modulo WHERE codigo = :codigo", nativeQuery = true)
    Integer findModuleIdByCode(@Param("codigo") String codigo);

    @Query(value = "SELECT nombre, fechaproceso, estado, registros, errores, cargadosanterior, porcargar, id_Modulo "
            + "FROM dbo.TBL_Archivo_Cargue WHERE estado = :estado AND id_Modulo = :idModulo", nativeQuery = true)
    List<ArchivoCargueTBL> findByEstadoAndModule(@Param("estado") String estado,
                                                 @Param("idModulo") Integer idModulo);

    @Procedure(procedureName = "dbo.SP_Valida_Movimientos_Siniestros")
    void executeMovementValidation(@Param("codigo_modulo") String codigoModulo);

    @Modifying
    @Transactional
    @Query(value = "UPDATE dbo.TBL_Archivo_Cargue SET estado = 'ELIMINADO' "
            + "WHERE estado = 'PENDIENTE' AND nombre = :nombreArchivo AND id_Modulo = :idModulo",
            nativeQuery = true)
    int markAsDeletedByFileName(@Param("nombreArchivo") String fileName,
                                @Param("idModulo") Integer idModulo);

    @Procedure(procedureName = "dbo.SP_Inserta_Movimientos_Siniestros")
    void insertMovements(@Param("nombrearchivo") String fileName,
                         @Param("codigo_modulo") String codigoModulo);

    @Query(value = "SELECT count(*) FROM dbo.TBL_Archivo_Cargue "
            + "WHERE estado = 'PENDIENTE' AND id_Modulo = :idModulo", nativeQuery = true)
    int getFilePending(@Param("idModulo") Integer idModulo);

    @Query(value = "SELECT count(*) FROM dbo.TBL_Error "
            + "WHERE campo2 = 'VALIDANDO_CARGUE' AND campo1 = "
            + "(SELECT MAX(id_archivo_cargue) FROM dbo.TBL_Archivo_Cargue "
            + " WHERE id_Modulo = :idModulo AND estado = 'PENDIENTE')", nativeQuery = true)
    int countValidationErrors(@Param("idModulo") Integer idModulo);

    @Modifying
    @Transactional
    @Query(value = "DELETE FROM dbo.TBL_Archivo_Cargue WHERE id_archivo_cargue = "
            + "(SELECT MAX(id_archivo_cargue) FROM dbo.TBL_Archivo_Cargue "
            + " WHERE id_Modulo = :idModulo AND estado = 'PENDIENTE')", nativeQuery = true)
    void deleteLastPending(@Param("idModulo") Integer idModulo);
}





package co.com.bnpparibas.cardif.closingclaims.infraestructure.repository;

import co.com.bnpparibas.cardif.closingclaims.domain.entity.TBLTmpValidaCargueOnbase;
import co.com.bnpparibas.cardif.closingclaims.domain.entity.TmpOnbaseId;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.*;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;

@Repository
public interface TBLTmpValidaCargueOnbaseRepository extends JpaRepository<TBLTmpValidaCargueOnbase, TmpOnbaseId> {

    Page<TBLTmpValidaCargueOnbase> findByError(Integer error, Pageable pageable);

    @Modifying
    @Transactional
    @Query(value = "TRUNCATE TABLE dbo.TBL_Tmp_Valida_Cargue_Onbase", nativeQuery = true)
    void truncateTable();
}

private static final String MODULE_CODE = "centro_america";

    @Override
    public String uploadMovements(String pHeader, String correlationId, String requestId, MultipartFile file, String user, String flagCountry) {
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

        if (fileUploadRepository.getFilePending(moduleId) != 0) {
            throw new BusinessException(null, "Error: Debe primero gestionar el archivo pendiente.", HttpStatus.PRECONDITION_FAILED);
        }

        tmpValidaCargueOnbaseRepository.truncateTable();

        savePendingLoadFile(filename, moduleId);

        readExcelFile.processExcel(file, flagCountry);

        fileUploadRepository.executeMovementValidation(MODULE_CODE);

        if (fileUploadRepository.countValidationErrors(moduleId) > 0) {
            fileUploadRepository.deleteLastPending(moduleId);
            throw new BusinessException(null, "Error validando el archivo cargado.", HttpStatus.PRECONDITION_FAILED);
        }

        saveLogApplication(user);

        return "Cargado...";
    }

    @Transactional
    public void savePendingLoadFile(String filename, Integer moduleId) {
        fileUploadRepository.save(ArchivoCargueTBL.builder()
                .estado(StatusFileLoad.PENDIENTE.name())
                .idModulo(moduleId)
                .id(FileLoadId.builder().nombre(filename).fechaproceso(new Date()).build())
                .build());
    }

    
