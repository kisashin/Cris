import co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia.AvalReportFileDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.entity.ArchivoReporteAvalExcel;


    /**
     * Consulta el estado del reporte mensual de Aval.
     *
     * @param correlationId  identificador de correlación para trazabilidad.
     * @param requestId      identificador de la petición.
     * @return estado del reporte y movimientos pendientes.
     */
    @GetMapping(
            path = "/aval-closing/report/status",
            produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResponseModel<AvalReportFileDTO>>
            findReportStatus(
            @RequestHeader(value = "correlation_id", required = false) String correlationId,
            @RequestHeader(value = "request_id", required = false) String requestId) {

        AvalReportFileDTO status =
                closingAvalService.findReportStatus(
                        correlationId,
                        requestId);

        ResponseModel<AvalReportFileDTO> response =
                new ResponseModel<>(correlationId,
                        ResponseHeader.builder()
                                .returnCode(HttpStatus.OK.value()).build(),
                        status);
        return new ResponseEntity<>(response, HttpStatus.OK);
    }

    /**
     * Genera y persiste el reporte mensual de Aval.
     *
     * @param pHeader        encabezado opcional de seguridad.
     * @param correlationId  identificador de correlación para trazabilidad.
     * @param requestId      identificador de la petición.
     * @return estado del reporte generado.
     */
    @PutMapping(
            path = "/aval-closing/report/generate",
            produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResponseModel<AvalReportFileDTO>>
            generateAvalReport(
            @RequestHeader(value = "_p", required = false) String pHeader,
            @RequestHeader(value = "correlation_id", required = false) String correlationId,
            @RequestHeader(value = "request_id", required = false) String requestId) {

        AvalReportFileDTO result =
                closingAvalService.generateAvalReport(
                        pHeader,
                        correlationId,
                        requestId);

        ResponseModel<AvalReportFileDTO> response =
                new ResponseModel<>(correlationId,
                        ResponseHeader.builder()
                                .returnCode(HttpStatus.OK.value()).build(),
                        result);
        return new ResponseEntity<>(response, HttpStatus.OK);
    }

    /**
     * Descarga el reporte mensual de Aval persistido.
     *
     * @param id             identificador del reporte.
     * @param correlationId  identificador de correlación para trazabilidad.
     * @param requestId      identificador de la petición.
     * @return contenido del archivo Excel.
     */
    @GetMapping(
            path = "/aval-closing/report/{id}/download",
            produces = EXCEL_CONTENT_TYPE)
    public ResponseEntity<byte[]> downloadAvalReport(
            @PathVariable("id") Integer id,
            @RequestHeader(value = "correlation_id", required = false) String correlationId,
            @RequestHeader(value = "request_id", required = false) String requestId) {

        ArchivoReporteAvalExcel file = closingAvalService.findReportFile(
                id,
                correlationId,
                requestId);

        byte[] content = file.getContenido();

        return ResponseEntity.ok()
                .header(
                        HttpHeaders.CONTENT_DISPOSITION,
                        "attachment; filename=\""
                                + file.getNombreArchivo() + "\"")
                .contentType(MediaType.parseMediaType(EXCEL_CONTENT_TYPE))
                .contentLength(content.length)
                .body(content);
    }
