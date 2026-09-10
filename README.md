import co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia.AvalReportFileDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.entity.ArchivoReporteAvalExcel;
import co.com.bnpparibas.cardif.closingclaims.infraestructure.repository.ArchivoReporteAvalExcelRepository;


    private static final String REPORT_FILE_NAME =
            "RPT_CIERRE_AVAL.xlsx";


    private final ArchivoReporteAvalExcelRepository reportFileRepository;



    public ClosingAvalServiceImpl(
            ClosingAvalRepository closingAvalRepository,
            ArchivoAsientoAvalXmlRepository fileRepository,
            AvalReportRepository reportRepository,
            ArchivoReporteAvalExcelRepository reportFileRepository,
            ColombiaAccountingXmlHelper xmlHelper,
            AvalReportExcelHelper excelHelper,
            StoredProcedureExecutor storedProcedureExecutor) {
        this.closingAvalRepository = closingAvalRepository;
        this.fileRepository = fileRepository;
        this.reportRepository = reportRepository;
        this.reportFileRepository = reportFileRepository;
        this.xmlHelper = xmlHelper;
        this.excelHelper = excelHelper;
        this.storedProcedureExecutor = storedProcedureExecutor;
    }



    @Override
    @Transactional(readOnly = true)
    public AvalReportFileDTO findReportStatus(
            String correlationId,
            String requestId) {

        int pending = countPendingMovements(correlationId, requestId);
        ArchivoReporteAvalExcel file =
                findLatestReportFile(correlationId, requestId);

        return toReportDto(file, pending);
    }

    @Override
    @Transactional
    public AvalReportFileDTO generateAvalReport(
            String pHeader,
            String correlationId,
            String requestId) {

        executeReportProcedure(correlationId, requestId);

        List<AvalReportRow> rows =
                findReportRows(correlationId, requestId);

        byte[] content = generateExcel(rows, correlationId, requestId);

        deletePreviousReportFiles(correlationId, requestId);

        ArchivoReporteAvalExcel saved = saveReportFile(
                content, rows.size(), correlationId, requestId);

        int pending = countPendingMovements(correlationId, requestId);

        return toReportDto(saved, pending);
    }

    @Override
    @Transactional(readOnly = true)
    public ArchivoReporteAvalExcel findReportFile(
            Integer id,
            String correlationId,
            String requestId) {

        ArchivoReporteAvalExcel file;

        try {
            file = reportFileRepository.findById(id).orElse(null);
        } catch (DataAccessException exception) {
            logDatabaseError(
                    "Error consultando el reporte de Aval",
                    correlationId,
                    requestId,
                    exception);
            throw reportDatabaseException(exception);
        }

        if (file == null || file.getContenido() == null) {
            throw new BusinessException(
                    null,
                    AvalReportMessage.REPORT_FILE_NOT_FOUND.getMessage(),
                    HttpStatus.NOT_FOUND);
        }

        return file;
    }

    private int countPendingMovements(
            String correlationId,
            String requestId) {
        try {
            return reportRepository.countPendingMovements();
        } catch (DataAccessException exception) {
            logDatabaseError(
                    "Error consultando los movimientos pendientes de Aval",
                    correlationId,
                    requestId,
                    exception);
            throw reportDatabaseException(exception);
        }
    }

    private ArchivoReporteAvalExcel findLatestReportFile(
            String correlationId,
            String requestId) {
        try {
            List<ArchivoReporteAvalExcel> files =
                    reportFileRepository.findLatest();

            return files.isEmpty() ? null : files.get(0);
        } catch (DataAccessException exception) {
            logDatabaseError(
                    "Error consultando el reporte generado de Aval",
                    correlationId,
                    requestId,
                    exception);
            throw reportDatabaseException(exception);
        }
    }

    private void deletePreviousReportFiles(
            String correlationId,
            String requestId) {
        try {
            reportFileRepository.deleteAllFiles();
        } catch (DataAccessException exception) {
            logDatabaseError(
                    "Error eliminando el reporte anterior de Aval",
                    correlationId,
                    requestId,
                    exception);
            throw reportDatabaseException(exception);
        }
    }

    private ArchivoReporteAvalExcel saveReportFile(
            byte[] content,
            int rowCount,
            String correlationId,
            String requestId) {

        ArchivoReporteAvalExcel file = ArchivoReporteAvalExcel.builder()
                .idLote(UUID.randomUUID().toString())
                .periodo(LocalDateTime.now()
                        .format(DateTimeFormatter.ofPattern("yyyyMM")))
                .nombreArchivo(REPORT_FILE_NAME)
                .contenido(content)
                .cantidadFilas(rowCount)
                .fechaproceso(LocalDateTime.now())
                .estado(GENERATED_STATUS)
                .build();

        try {
            return reportFileRepository.save(file);
        } catch (DataAccessException exception) {
            logDatabaseError(
                    "Error guardando el reporte de Aval",
                    correlationId,
                    requestId,
                    exception);
            throw reportDatabaseException(exception);
        }
    }

    private AvalReportFileDTO toReportDto(
            ArchivoReporteAvalExcel file,
            int pending) {

        if (file == null) {
            return AvalReportFileDTO.builder()
                    .pendingMovements(pending)
                    .build();
        }

        return AvalReportFileDTO.builder()
                .id(file.getId())
                .period(file.getPeriodo())
                .fileName(file.getNombreArchivo())
                .rowCount(file.getCantidadFilas())
                .processDate(file.getFechaproceso() == null
                        ? null
                        : file.getFechaproceso().format(PROCESS_DATE_FORMAT))
                .status(file.getEstado())
                .pendingMovements(pending)
                .build();
    }
