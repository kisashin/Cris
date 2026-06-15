src/main/java/co/com/bnpparibas/cardif/closingclaims/domain/services/IPeruAccountingReportService.java

package co.com.bnpparibas.cardif.closingclaims.domain.services;

import co.com.bnpparibas.cardif.closingclaims.domain.dtos.peruaccountingreport.PeruAccountingReportResponseDTO;

/**
 * Servicio para gestionar el reporte contable de Perú.
 */
public interface IPeruAccountingReportService {

    /**
     * Consulta la fecha de la última generación del reporte.
     *
     * @param pHeader encabezado de seguridad.
     * @param correlationId identificador de correlación.
     * @param requestId identificador de la solicitud.
     * @return fecha de la última generación.
     */
    PeruAccountingReportResponseDTO getLatestReportDate(
            String pHeader,
            String correlationId,
            String requestId);

    /**
     * Genera la información del reporte contable.
     *
     * @param pHeader encabezado de seguridad.
     * @param correlationId identificador de correlación.
     * @param requestId identificador de la solicitud.
     * @return mensaje con el resultado del proceso.
     */
    String generateReport(
            String pHeader,
            String correlationId,
            String requestId);

    /**
     * Genera el archivo Excel del reporte contable.
     *
     * @param pHeader encabezado de seguridad.
     * @param correlationId identificador de correlación.
     * @param requestId identificador de la solicitud.
     * @return contenido del archivo Excel.
     */
    byte[] downloadReport(
            String pHeader,
            String correlationId,
            String requestId);
}
