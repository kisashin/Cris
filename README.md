import co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia.AvalReportStatusDTO;

    private static final String EXCEL_CONTENT_TYPE =
            "application/vnd.openxmlformats-officedocument"
                    + ".spreadsheetml.sheet";

    private static final String REPORT_FILE_NAME =
            "RPT_CIERRE_AVAL.xlsx";



            


    /**
     * Consulta el estado del reporte mensual de Aval.
     *
     * @param correlationId  identificador de correlación para trazabilidad.
     * @param requestId      identificador de la petición.
     * @return estado del reporte con los movimientos pendientes.
     */
    @GetMapping(
            path = "/aval-closing/report/status",
            produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResponseModel<AvalReportStatusDTO>>
            findReportStatus(
            @RequestHeader(value = "correlation_id", required = false) String correlationId,
            @RequestHeader(value = "request_id", required = false) String requestId) {

        AvalReportStatusDTO status =
                closingAvalService.findReportStatus(
                        correlationId,
                        requestId);

        ResponseModel<AvalReportStatusDTO> response =
                new ResponseModel<>(correlationId,
                        ResponseHeader.builder()
                                .returnCode(HttpStatus.OK.value()).build(),
                        status);
        return new ResponseEntity<>(response, HttpStatus.OK);
    }

    /**
     * Descarga el reporte mensual de Aval en formato Excel.
     *
     * @param pHeader        encabezado opcional de seguridad.
     * @param correlationId  identificador de correlación para trazabilidad.
     * @param requestId      identificador de la petición.
     * @return contenido del archivo Excel.
     */
    @GetMapping(
            path = "/aval-closing/report/download",
            produces = EXCEL_CONTENT_TYPE)
    public ResponseEntity<byte[]> downloadAvalReport(
            @RequestHeader(value = "_p", required = false) String pHeader,
            @RequestHeader(value = "correlation_id", required = false) String correlationId,
            @RequestHeader(value = "request_id", required = false) String requestId) {

        byte[] content = closingAvalService.downloadAvalReport(
                pHeader,
                correlationId,
                requestId);

        return ResponseEntity.ok()
                .header(
                        HttpHeaders.CONTENT_DISPOSITION,
                        "attachment; filename=\""
                                + REPORT_FILE_NAME + "\"")
                .contentType(MediaType.parseMediaType(EXCEL_CONTENT_TYPE))
                .contentLength(content.length)
                .body(content);
    }            
