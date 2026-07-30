package co.com.bnpparibas.cardif.closingclaims.infraestructure.repository;

import co.com.bnpparibas.cardif.closingclaims.domain.entity.ArchivoDatosEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;

public interface ReportDataRepository extends JpaRepository<ArchivoDatosEntity, Integer> {

    /** Retrieves the report execution status. */
    @Query(value = "SELECT id, "
            + " fechaproceso, "
            + " estado "
            + "FROM dbo.TBL_Archivo_Datos "
            + "ORDER BY id DESC", nativeQuery = true)
    List<ReportStatusProjection> findAllReportStatus();

    /** Executes report generation. */
    @Modifying
    @Transactional
    @Query(value = "EXEC dbo.sp_Genera_Datos_Siniestros", nativeQuery = true)
    void generateReport();

    /** Retrieves report status by id. */
    @Query(value = "SELECT id, "
            + " nombredatos, "
            + " nombremov, "
            + " fechaproceso, "
            + " estado "
            + "FROM dbo.TBL_Archivo_Datos "
            + "WHERE id = :id", nativeQuery = true)
    ReportDetailProjection findReportById(Integer id);

    /** Retrieves inconsistent coverages. */
    @Query(value = "SELECT DISTINCT "
            + " H1.Llavesiniestro AS Llavesiniestros "
            + "FROM TBL_Historico_Movimientos H1 "
            + "LEFT JOIN tbl_historico_inicial H2 "
            + " ON H1.Llavesiniestro = H2.Llavesiniestro "
            + "WHERE H2.Llavesiniestro IS NULL", nativeQuery = true)
    List<InconsistentCoverageProjection> findInconsistentCoverages();

    /** Report status projection. */
    interface ReportStatusProjection {
        Integer getId();
        LocalDateTime getFechaproceso();
        String getEstado();
    }

    /** Report detail projection. */
    interface ReportDetailProjection {
        Integer getId();
        String getNombredatos();
        String getNombremov();
        LocalDateTime getFechaproceso();
        String getEstado();
    }

    /** Inconsistent coverage projection. */
    interface InconsistentCoverageProjection {
        String getLlavesiniestros();
    }
}
