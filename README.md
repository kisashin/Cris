CardifPeruClosingRepository

package co.com.bnpparibas.cardif.closingclaims.infraestructure.repository;

import co.com.bnpparibas.cardif.closingclaims.domain.entity.CardifPeruClosing;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * Repositorio para el cierre de movimientos Cardif Perú (legacy {@code _ext}).
 *
 * <p>La lectura del reporte se hace contra la vista {@code dbo.vw_mov_cardif_ext}.
 * El conteo de pendientes y la ejecución del procedimiento se hacen contra la
 * tabla real {@code dbo.historicomovimientos_ext}.</p>
 */
@Repository
public interface CardifPeruClosingRepository
        extends JpaRepository<CardifPeruClosing, Long>,
        CardifPeruClosingRepositoryCustom {

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
                    + "FROM dbo.historicomovimientos_ext "
                    + "WHERE Fechacontabilizacion IS NULL "
                    + "OR LTRIM(RTRIM(Fechacontabilizacion)) = ''",
            nativeQuery = true)
    long countPendingMovements();

    /**
     * Consulta todos los movimientos para generar el archivo Excel.
     *
     * @return registros de la vista del reporte.
     */
    @Query(
            value = "SELECT * "
                    + "FROM dbo.vw_mov_cardif_ext "
                    + "ORDER BY IDCARVAJAL",
            nativeQuery = true)
    List<CardifPeruClosing> findAllForExport();
}
