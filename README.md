CardifPeruClosingRepositoryCustom

package co.com.bnpparibas.cardif.closingclaims.infraestructure.repository;

/**
 * Fragmento personalizado del repositorio para ejecutar el procedimiento
 * almacenado de contabilización.
 *
 * <p>El procedimiento {@code dbo.sp_contabiliza_cardif_ext} devuelve un
 * result-set, por lo que NO puede invocarse con el patrón
 * {@code @Modifying @Query void} (Hibernate espera un update-count y falla
 * al recibir filas). Por eso se ejecuta vía {@code JdbcTemplate} en la
 * implementación, que tolera tanto result-sets como update-counts.</p>
 */
public interface CardifPeruClosingRepositoryCustom {

    /**
     * Ejecuta el procedimiento que contabiliza los movimientos pendientes.
     * El result-set que devuelve el procedimiento se ignora, igual que el
     * legacy.
     */
    void executeAccountingProcedure();
}
