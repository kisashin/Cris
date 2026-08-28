import co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia.AvalReportRow;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia.AvalReportStatusDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.util.helpers.AvalReportExcelHelper;
import co.com.bnpparibas.cardif.closingclaims.domain.util.messages.AvalReportMessage;
import co.com.bnpparibas.cardif.closingclaims.infraestructure.repository.AvalReportRepository;

import java.io.IOException;
import java.math.BigDecimal;


    private static final String REPORT_PROCEDURE_CALL =
            "EXEC dbo.sp_Genera_RepAval_cierre";

    private static final String REPORT_QUERY =
            "SELECT compania,sucursal,descripcion_ramo,symbol,ramo2,"
                    + "nro_poliza,modulo,cod_banco_negocio,"
                    + "DESCRIPCION_TOMADOR,poliza_lider_alfa,"
                    + "SINIESTRO_LIDER,valor,NUMERO_LOTE,CAMPO_UNION,"
                    + "VALOR_INICIAL_RESERVA,VALOR_AJUSTES_RESERVA,"
                    + "VALOR_PAGOS,VALOR_ACTUAL_RESERVA,PORCENTAJE_ALFA,"
                    + "VALOR_GASTOS_COASEGURO,VALOR_SALVAMENTO,"
                    + "VALOR_RECUPERACIONES,Nroidentificacion,"
                    + "Nombreasegurado,fechanacimiento,edad,SEXO,Profesion,"
                    + "fechaperdida,fechaaviso,fechareclamo,CODIGO_CAUSA,"
                    + "causa_siniestro,ciudad,Tipo_siniestro,nro_credito,"
                    + "fechadesembolso,porcentaje_asegurabilidad,"
                    + "tipocredito,cobertura_lider,reportado_por,"
                    + "Nit_beneficiario,Beneficiario,causal_objecion,"
                    + "fecha_objecion,PLACA_,SERIAL_,MOTOR_,TIPO_VEHICULO,"
                    + "CLASE_VEHICULO,OBSERVACIONES_PAGO "
                    + "FROM dbo.tmp_repavalcierre";

    private static final String REPORT_REQUIRED_COLUMN = "compania";







        private final ClosingAvalRepository closingAvalRepository;
    private final ArchivoAsientoAvalXmlRepository fileRepository;
    private final AvalReportRepository reportRepository;
    private final ColombiaAccountingXmlHelper xmlHelper;
    private final AvalReportExcelHelper excelHelper;
    private final StoredProcedureExecutor storedProcedureExecutor;

    public ClosingAvalServiceImpl(
            ClosingAvalRepository closingAvalRepository,
            ArchivoAsientoAvalXmlRepository fileRepository,
            AvalReportRepository reportRepository,
            ColombiaAccountingXmlHelper xmlHelper,
            AvalReportExcelHelper excelHelper,
            StoredProcedureExecutor storedProcedureExecutor) {
        this.closingAvalRepository = closingAvalRepository;
        this.fileRepository = fileRepository;
        this.reportRepository = reportRepository;
        this.xmlHelper = xmlHelper;
        this.excelHelper = excelHelper;
        this.storedProcedureExecutor = storedProcedureExecutor;
    }












        @Override
    @Transactional(readOnly = true)
    public AvalReportStatusDTO findReportStatus(
            String correlationId,
            String requestId) {

        int pending;

        try {
            pending = reportRepository.countPendingMovements();
        } catch (DataAccessException exception) {
            logDatabaseError(
                    "Error consultando los movimientos pendientes de Aval",
                    correlationId,
                    requestId,
                    exception);
            throw reportDatabaseException(exception);
        }

        return AvalReportStatusDTO.builder()
                .generationDate(
                        LocalDateTime.now().format(PROCESS_DATE_FORMAT))
                .pendingMovements(pending)
                .build();
    }

    @Override
    @Transactional
    public byte[] downloadAvalReport(
            String pHeader,
            String correlationId,
            String requestId) {

        executeReportProcedure(correlationId, requestId);

        List<AvalReportRow> rows =
                findReportRows(correlationId, requestId);

        if (rows.isEmpty()) {
            throw new BusinessException(
                    null,
                    AvalReportMessage.NO_MOVEMENTS_TO_EXPORT.getMessage(),
                    HttpStatus.NOT_FOUND);
        }

        return generateExcel(rows, correlationId, requestId);
    }

    private void executeReportProcedure(
            String correlationId,
            String requestId) {
        try {
            storedProcedureExecutor.query(
                    REPORT_PROCEDURE_CALL,
                    resultSet -> null,
                    REPORT_REQUIRED_COLUMN);
        } catch (DataAccessException exception) {
            logDatabaseError(
                    "Error ejecutando la generación del reporte de Aval",
                    correlationId,
                    requestId,
                    exception);
            throw reportDatabaseException(exception);
        }
    }

    private List<AvalReportRow> findReportRows(
            String correlationId,
            String requestId) {
        try {
            return storedProcedureExecutor.query(
                    REPORT_QUERY,
                    resultSet -> AvalReportRow.builder()
                            .compania(resultSet.getString("compania"))
                            .sucursal(resultSet.getString("sucursal"))
                            .descripcionRamo(
                                    resultSet.getString("descripcion_ramo"))
                            .symbol(resultSet.getString("symbol"))
                            .ramo2(readInteger(resultSet, "ramo2"))
                            .nroPoliza(resultSet.getString("nro_poliza"))
                            .modulo(resultSet.getString("modulo"))
                            .codBancoNegocio(
                                    resultSet.getString("cod_banco_negocio"))
                            .descripcionTomador(resultSet
                                    .getString("DESCRIPCION_TOMADOR"))
                            .polizaLiderAlfa(
                                    resultSet.getString("poliza_lider_alfa"))
                            .siniestroLider(
                                    resultSet.getString("SINIESTRO_LIDER"))
                            .valor(readInteger(resultSet, "valor"))
                            .numeroLote(
                                    readInteger(resultSet, "NUMERO_LOTE"))
                            .campoUnion(resultSet.getString("CAMPO_UNION"))
                            .valorInicialReserva(resultSet
                                    .getBigDecimal("VALOR_INICIAL_RESERVA"))
                            .valorAjustesReserva(resultSet
                                    .getBigDecimal("VALOR_AJUSTES_RESERVA"))
                            .valorPagos(
                                    resultSet.getBigDecimal("VALOR_PAGOS"))
                            .valorActualReserva(resultSet
                                    .getBigDecimal("VALOR_ACTUAL_RESERVA"))
                            .porcentajeAlfa(
                                    readInteger(resultSet, "PORCENTAJE_ALFA"))
                            .valorGastosCoaseguro(readInteger(
                                    resultSet, "VALOR_GASTOS_COASEGURO"))
                            .valorSalvamento(readInteger(
                                    resultSet, "VALOR_SALVAMENTO"))
                            .valorRecuperaciones(readInteger(
                                    resultSet, "VALOR_RECUPERACIONES"))
                            .nroidentificacion(
                                    resultSet.getString("Nroidentificacion"))
                            .nombreasegurado(
                                    resultSet.getString("Nombreasegurado"))
                            .fechanacimiento(
                                    resultSet.getString("fechanacimiento"))
                            .edad(readInteger(resultSet, "edad"))
                            .sexo(resultSet.getString("SEXO"))
                            .profesion(resultSet.getString("Profesion"))
                            .fechaperdida(
                                    resultSet.getString("fechaperdida"))
                            .fechaaviso(resultSet.getString("fechaaviso"))
                            .fechareclamo(
                                    resultSet.getString("fechareclamo"))
                            .codigoCausa(
                                    resultSet.getString("CODIGO_CAUSA"))
                            .causaSiniestro(
                                    resultSet.getString("causa_siniestro"))
                            .ciudad(resultSet.getString("ciudad"))
                            .tipoSiniestro(
                                    resultSet.getString("Tipo_siniestro"))
                            .nroCredito(resultSet.getString("nro_credito"))
                            .fechadesembolso(
                                    resultSet.getString("fechadesembolso"))
                            .porcentajeAsegurabilidad(resultSet
                                    .getString("porcentaje_asegurabilidad"))
                            .tipocredito(resultSet.getString("tipocredito"))
                            .coberturaLider(
                                    resultSet.getString("cobertura_lider"))
                            .reportadoPor(
                                    resultSet.getString("reportado_por"))
                            .nitBeneficiario(
                                    resultSet.getString("Nit_beneficiario"))
                            .beneficiario(
                                    resultSet.getString("Beneficiario"))
                            .causalObjecion(
                                    resultSet.getString("causal_objecion"))
                            .fechaObjecion(
                                    resultSet.getString("fecha_objecion"))
                            .placa(resultSet.getString("PLACA_"))
                            .serial(resultSet.getString("SERIAL_"))
                            .motor(resultSet.getString("MOTOR_"))
                            .tipoVehiculo(
                                    resultSet.getString("TIPO_VEHICULO"))
                            .claseVehiculo(
                                    resultSet.getString("CLASE_VEHICULO"))
                            .observacionesPago(resultSet
                                    .getString("OBSERVACIONES_PAGO"))
                            .build(),
                    REPORT_REQUIRED_COLUMN);
        } catch (DataAccessException exception) {
            logDatabaseError(
                    "Error consultando el reporte de Aval",
                    correlationId,
                    requestId,
                    exception);
            throw reportDatabaseException(exception);
        }
    }

    private Integer readInteger(
            java.sql.ResultSet resultSet,
            String column) throws java.sql.SQLException {

        int value = resultSet.getInt(column);
        return resultSet.wasNull() ? null : value;
    }

    private byte[] generateExcel(
            List<AvalReportRow> rows,
            String correlationId,
            String requestId) {
        try {
            return excelHelper.generateExcel(rows);
        } catch (IOException exception) {
            log.error(
                    "Error generando Excel. correlationId={}, requestId={}",
                    correlationId,
                    requestId,
                    exception);
            throw new BusinessException(
                    exception,
                    null,
                    AvalReportMessage.EXCEL_GENERATION_ERROR.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    private BusinessException reportDatabaseException(
            DataAccessException exception) {
        return new BusinessException(
                exception,
                null,
                AvalReportMessage.DATABASE_ACCESS_ERROR.getMessage(),
                HttpStatus.INTERNAL_SERVER_ERROR);
    }
