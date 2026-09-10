    /**
     * Consulta el estado del reporte mensual de Aval.
     */
    AvalReportFileDTO findReportStatus(
            String correlationId, String requestId);

    /**
     * Genera y persiste el reporte mensual de Aval.
     */
    AvalReportFileDTO generateAvalReport(
            String pHeader, String correlationId, String requestId);

    /**
     * Descarga el reporte mensual de Aval persistido.
     */
    ArchivoReporteAvalExcel findReportFile(
            Integer id, String correlationId, String requestId);
