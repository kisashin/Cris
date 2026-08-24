package co.com.bnpparibas.cardif.closingclaims.infraestructure.repository;

import co.com.bnpparibas.cardif.closingclaims.domain.entity.CardifCenterClosing;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * Repositorio para el cierre de movimientos Cardif Centroamerica.
 */
@Repository
public interface CardifCenterClosingRepository
        extends JpaRepository<CardifCenterClosing, Long> {

    /**
     * Consulta todos los movimientos para generar el archivo Excel.
     *
     * @return registros de la vista del reporte.
     */
    @Query(
            value = "SELECT * "
                    + "FROM dbo.vw_mov_cardif_cen "
                    + "ORDER BY IDCARVAJAL",
            nativeQuery = true)
    List<CardifCenterClosing> findAllForExport();
}
