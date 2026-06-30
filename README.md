@Value("${cardif.center.closing.report-filename:ReporteMovimientosCentro.xlsx}")
private String fileName;

"attachment; filename=\"" + fileName + "\"")

cardif:
  center:
    closing:
      report-filename: ReporteMovimientosCentro.xlsx
