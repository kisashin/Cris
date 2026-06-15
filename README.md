PeruAccountingReportRepository

package co.com.bnpparibas.cardif.closingclaims.infraestructure.repository;

import co.com.bnpparibas.cardif.closingclaims.domain.entity.PeruAccountingReport;
import co.com.bnpparibas.cardif.closingclaims.domain.entity.PeruAccountingReportId;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

/**
 * Repositorio para la consulta y generación del reporte contable de Perú.
 */
@Repository
public interface PeruAccountingReportRepository
        extends JpaRepository<PeruAccountingReport, PeruAccountingReportId> {

    /**
     * Consulta la fecha más reciente de generación del reporte.
     *
     * @return fecha de la última generación.
     */
    @Query(
            value = "SELECT MAX(FechaReporte) " +
                    "FROM dbo.reportecontable_peru",
            nativeQuery = true
    )
    LocalDateTime findLatestReportDate();

    /**
     * Ejecuta el procedimiento almacenado que reconstruye el reporte.
     */
    @Modifying(clearAutomatically = true, flushAutomatically = true)
    @Query(
            value = "EXEC dbo.SP_ReporteContablePeru",
            nativeQuery = true
    )
    void generateReport();

    /**
     * Consulta todos los registros utilizados para generar el archivo Excel.
     *
     * @return registros del reporte contable.
     */
    @Query(
            value = "SELECT * " +
                    "FROM dbo.reportecontable_peru " +
                    "ORDER BY NumeroSiniestro, Fechamovimiento2",
            nativeQuery = true
    )
    List<PeruAccountingReport> findAllForExport();
}
