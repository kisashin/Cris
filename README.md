ICardifCenterClosingService

package co.com.bnpparibas.cardif.closingclaims.domain.services;

/**
 * Servicio para el cierre de movimientos Cardif Centroamérica (legacy Centroamérica).
 */
public interface ICardifCenterClosingService {

    /**
     * Ejecuta la contabilización de los movimientos pendientes.
     *
     * <p>Replica el comportamiento del botón "Genera XML" del legacy: si hay
     * pendientes, ejecuta el procedimiento; si no, informa que no hay
     * movimientos.</p>
     *
     * @param pHeader encabezado de seguridad.
     * @param correlationId identificador de correlación.
     * @param requestId identificador de la solicitud.
     * @return mensaje con el resultado del proceso.
     */
    String generateAccountingEntries(
            String pHeader,
            String correlationId,
            String requestId);

    /**
     * Genera el archivo Excel del reporte de movimientos.
     *
     * @param pHeader encabezado de seguridad.
     * @param correlationId identificador de correlación.
     * @param requestId identificador de la solicitud.
     * @return contenido binario del archivo Excel.
     */
    byte[] downloadMovementsReport(
            String pHeader,
            String correlationId,
            String requestId);
}
