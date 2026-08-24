package co.com.bnpparibas.cardif.closingclaims.domain.services;

import co.com.bnpparibas.cardif.closingclaims.domain.dtos.cardifcenterclosing.CenterAccountingResultDTO;

/**
 * Servicio para el cierre de movimientos Cardif Centroamerica.
 */
public interface ICardifCenterClosingService {

    /**
     * Ejecuta la contabilizacion de los movimientos pendientes y devuelve los
     * archivos XML generados por tipo de movimiento.
     *
     * @param pHeader encabezado de seguridad.
     * @param correlationId identificador de correlacion.
     * @param requestId identificador de la solicitud.
     * @return resultado del proceso con los archivos en Base64.
     */
    CenterAccountingResultDTO generateAccountingEntries(
            String pHeader,
            String correlationId,
            String requestId);

    /**
     * Genera el archivo Excel del reporte de movimientos.
     *
     * @param pHeader encabezado de seguridad.
     * @param correlationId identificador de correlacion.
     * @param requestId identificador de la solicitud.
     * @return contenido binario del archivo Excel.
     */
    byte[] downloadMovementsReport(
            String pHeader,
            String correlationId,
            String requestId);
}

