    /**
     * Consulta el estado del reporte mensual de Aval.
     */
    AvalReportStatusDTO findReportStatus(
            String correlationId, String requestId);

    /**
     * Genera el reporte mensual de Aval en formato Excel.
     */
    byte[] downloadAvalReport(
            String pHeader, String correlationId, String requestId);


  import co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia.AvalReportStatusDTO;          
