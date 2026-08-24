package co.com.bnpparibas.cardif.closingclaims.domain.services;

import co.com.bnpparibas.cardif.closingclaims.domain.dtos.cardifcenterclosing.AccountingXmlFileDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.cardifcenterclosing.CenterAccountingResultDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.entity.ArchivoAsientoCentro;

import java.util.List;

/**
 * Servicio para el cierre de movimientos Cardif Centroamerica.
 */
public interface ICardifCenterClosingService {

    /**
     * Ejecuta la contabilizacion de los movimientos pendientes y persiste los
     * archivos XML generados por tipo de movimiento.
     *
     * @param pHeader encabezado de seguridad.
     * @param correlationId identificador de correlacion.
     * @param requestId identificador de la solicitud.
     * @return resultado del proceso con los archivos generados.
     */
    CenterAccountingResultDTO generateAccountingEntries(
            String pHeader,
            String correlationId,
            String requestId);

    /**
     * Consulta los archivos XML generados en procesos anteriores.
     *
     * @param correlationId identificador de correlacion.
     * @param requestId identificador de la solicitud.
     * @return archivos disponibles para descarga.
     */
    List<AccountingXmlFileDTO> findGeneratedFiles(
            String correlationId,
            String requestId);

    /**
     * Consulta un archivo XML persistido por su identificador.
     *
     * @param id identificador del archivo.
     * @param correlationId identificador de correlacion.
     * @param requestId identificador de la solicitud.
     * @return archivo con su contenido.
     */
    ArchivoAsientoCentro findXmlFile(
            Integer id,
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
