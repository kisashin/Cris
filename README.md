CardifCenterClosingRepository

package co.com.bnpparibas.cardif.closingclaims.infraestructure.repository;

import co.com.bnpparibas.cardif.closingclaims.domain.entity.CardifCenterClosing;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * Repositorio para el cierre de movimientos Cardif Centroamérica (legacy Centroamérica).
 *
 * <p>La lectura del reporte se hace contra la vista {@code dbo.vw_mov_cardif_cen}.
 * El conteo de pendientes y la ejecución del procedimiento se hacen contra la
 * tabla real {@code dbo.TBL_Historico_Movimientos}.</p>
 */
@Repository
public interface CardifCenterClosingRepository
        extends JpaRepository<CardifCenterClosing, Long> {

    /**
     * Cuenta los movimientos pendientes por contabilizar.
     *
     * <p>Se conserva el doble criterio del legacy ({@code IS NULL} y cadena
     * vacía) porque {@code Fechacontabilizacion} es {@code varchar}, no
     * {@code datetime}; validar solo {@code IS NULL} dejaría fuera los
     * registros con cadena vacía.</p>
     *
     * @return cantidad de movimientos pendientes.
     */
    @Query(
            value = "SELECT COUNT(1) "
                    + "FROM dbo.TBL_Historico_Movimientos "
                    + "WHERE Fechacontabilizacion IS NULL "
                    + "OR LTRIM(RTRIM(Fechacontabilizacion)) = ''",
            nativeQuery = true)
    long countPendingMovements();

    /**
     * Ejecuta el procedimiento almacenado que contabiliza los movimientos
     * pendientes. Mismo patrón que el módulo Perú ({@code generateReport}).
     */
    @Modifying(clearAutomatically = true, flushAutomatically = true)
    @Query(
            value = "EXEC dbo.sp_contabiliza_cardifCentro",
            nativeQuery = true)
    void executeAccountingProcedure();

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
