package co.com.bnpparibas.cardif.closingclaims.domain.util.helpers;

import co.com.bnpparibas.cardif.closingclaims.domain.entity.PeruAccountingReport;
import org.apache.poi.ss.usermodel.Cell;
import org.apache.poi.ss.usermodel.CellStyle;
import org.apache.poi.ss.usermodel.FillPatternType;
import org.apache.poi.ss.usermodel.Font;
import org.apache.poi.ss.usermodel.HorizontalAlignment;
import org.apache.poi.ss.usermodel.IndexedColors;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.ss.usermodel.Workbook;
import org.apache.poi.ss.util.CellRangeAddress;
import org.apache.poi.xssf.streaming.SXSSFWorkbook;
import org.springframework.stereotype.Component;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.sql.Timestamp;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.function.Function;

/**
 * Helper encargado de generar el archivo Excel del reporte contable de Perú.
 */
@Component
public class PeruAccountingReportExcelHelper {

    private static final String SHEET_NAME = "Reporte Contable Peru";
    private static final String DATE_FORMAT = "dd/MM/yyyy HH:mm:ss";
    private static final int ROW_ACCESS_WINDOW_SIZE = 100;
    private static final int MINIMUM_COLUMN_WIDTH = 15;
    private static final int MAXIMUM_COLUMN_WIDTH = 40;

    private static final List<ExcelColumn> COLUMNS = createColumns();

    /**
     * Genera el archivo Excel con la información del reporte contable.
     *
     * @param reports registros que serán exportados.
     * @return contenido binario del archivo Excel.
     * @throws IOException cuando no es posible generar el archivo.
     */
    public byte[] generateExcel(List<PeruAccountingReport> reports)
            throws IOException {

        SXSSFWorkbook workbook = createWorkbook();

        try {
            return writeWorkbook(workbook, reports);
        } finally {
            closeWorkbook(workbook);
        }
    }

    SXSSFWorkbook createWorkbook() {
        SXSSFWorkbook workbook =
                new SXSSFWorkbook(ROW_ACCESS_WINDOW_SIZE);

        workbook.setCompressTempFiles(true);
        return workbook;
    }

    private byte[] writeWorkbook(
            SXSSFWorkbook workbook,
            List<PeruAccountingReport> reports) throws IOException {

        try (ByteArrayOutputStream outputStream =
                     new ByteArrayOutputStream()) {

            populateWorkbook(workbook, reports);
            workbook.write(outputStream);
            return outputStream.toByteArray();
        }
    }

    private void populateWorkbook(
            SXSSFWorkbook workbook,
            List<PeruAccountingReport> reports) {

        Sheet sheet = workbook.createSheet(SHEET_NAME);
        CellStyle headerStyle = createHeaderStyle(workbook);
        CellStyle dateStyle = createDateStyle(workbook);

        createHeaderRow(sheet, headerStyle);
        createDataRows(sheet, reports, dateStyle);
        configureSheet(sheet);
    }

    private CellStyle createHeaderStyle(Workbook workbook) {
        CellStyle style = workbook.createCellStyle();

        style.setFont(createHeaderFont(workbook));
        style.setFillForegroundColor(IndexedColors.DARK_GREEN.getIndex());
        style.setFillPattern(FillPatternType.SOLID_FOREGROUND);
        style.setAlignment(HorizontalAlignment.CENTER);
        style.setWrapText(true);

        return style;
    }

    private Font createHeaderFont(Workbook workbook) {
        Font font = workbook.createFont();

        font.setBold(true);
        font.setColor(IndexedColors.WHITE.getIndex());

        return font;
    }

    private CellStyle createDateStyle(Workbook workbook) {
        CellStyle style = workbook.createCellStyle();

        style.setDataFormat(
                workbook.getCreationHelper()
                        .createDataFormat()
                        .getFormat(DATE_FORMAT));

        return style;
    }

    private void createHeaderRow(
            Sheet sheet,
            CellStyle headerStyle) {

        Row headerRow = sheet.createRow(0);

        for (int index = 0; index < COLUMNS.size(); index++) {
            Cell cell = headerRow.createCell(index);
            cell.setCellValue(COLUMNS.get(index).getHeader());
            cell.setCellStyle(headerStyle);
        }
    }

    private void createDataRows(
            Sheet sheet,
            List<PeruAccountingReport> reports,
            CellStyle dateStyle) {

        int rowIndex = 1;

        for (PeruAccountingReport report : reports) {
            createDataRow(
                    sheet.createRow(rowIndex++),
                    report,
                    dateStyle);
        }
    }

    private void createDataRow(
            Row row,
            PeruAccountingReport report,
            CellStyle dateStyle) {

        for (int index = 0; index < COLUMNS.size(); index++) {
            Object value = COLUMNS.get(index).getValue(report);
            writeCell(row.createCell(index), value, dateStyle);
        }
    }

    private void writeCell(
            Cell cell,
            Object value,
            CellStyle dateStyle) {

        if (value == null) {
            cell.setBlank();
            return;
        }

        if (value instanceof Number) {
            cell.setCellValue(((Number) value).doubleValue());
            return;
        }

        if (value instanceof LocalDateTime) {
            writeDateCell(cell, (LocalDateTime) value, dateStyle);
            return;
        }

        if (value instanceof String) {
            cell.setCellValue((String) value);
            return;
        }

        if (value instanceof Boolean) {
            cell.setCellValue((Boolean) value);
            return;
        }

        throw new IllegalArgumentException(
                "Unsupported Excel cell value type: "
                        + value.getClass().getName()
        );
    }

    private void writeDateCell(
            Cell cell,
            LocalDateTime value,
            CellStyle dateStyle) {

        cell.setCellValue(Timestamp.valueOf(value));
        cell.setCellStyle(dateStyle);
    }

    private void configureSheet(Sheet sheet) {
        sheet.createFreezePane(0, 1);
        sheet.setAutoFilter(
                new CellRangeAddress(
                        0,
                        0,
                        0,
                        COLUMNS.size() - 1));

        configureColumnWidths(sheet);
    }

    private void configureColumnWidths(Sheet sheet) {
        for (int index = 0; index < COLUMNS.size(); index++) {
            int headerLength = COLUMNS.get(index).getHeader().length() + 2;
            int width = Math.max(MINIMUM_COLUMN_WIDTH, headerLength);
            width = Math.min(MAXIMUM_COLUMN_WIDTH, width);
            sheet.setColumnWidth(index, width * 256);
        }
    }

    private void closeWorkbook(SXSSFWorkbook workbook)
            throws IOException {

        try {
            workbook.close();
        } finally {
            workbook.dispose();
        }
    }

    private static List<ExcelColumn> createColumns() {
        List<ExcelColumn> columns = new ArrayList<>();

        addColumnsOne(columns);
        addColumnsTwo(columns);
        addColumnsThree(columns);
        addColumnsFour(columns);
        addColumnsFive(columns);
        addColumnsSix(columns);
        addColumnsSeven(columns);
        addColumnsEight(columns);
        addColumnsNine(columns);
        addColumnsTen(columns);
        addColumnsEleven(columns);
        addColumnsTwelve(columns);

        return Collections.unmodifiableList(columns);
    }

    private static void addColumnsOne(List<ExcelColumn> columns) {
        add(columns, "FechaAviso", PeruAccountingReport::getNoticeDate);
        add(columns, "MesNotificacion", PeruAccountingReport::getNotificationMonth);
        add(columns, "FechaAvisoCardif", PeruAccountingReport::getCardifNoticeDate);
        add(columns, "FechaAvisoSocio", PeruAccountingReport::getPartnerNoticeDate);
        add(columns, "NumeroSiniestro", PeruAccountingReportExcelHelper::getClaimNumber);
        add(columns, "FechaUltDocRecCardif", PeruAccountingReport::getLastDocumentReceivedDate);
        add(columns, "FechaPublicacion", PeruAccountingReport::getPublicationDate);
        add(columns, "Socio", PeruAccountingReport::getPartner);
        add(columns, "Producto", PeruAccountingReport::getProduct);
        add(columns, "CodProducto", PeruAccountingReport::getProductCode);
    }

    private static void addColumnsTwo(List<ExcelColumn> columns) {
        add(columns, "Certificado", PeruAccountingReport::getCertificate);
        add(columns, "FechaInicioPoliza", PeruAccountingReport::getPolicyStartDate);
        add(columns, "FechaFinPoliza", PeruAccountingReport::getPolicyEndDate);
        add(columns, "ValidacionEdadIngreso", PeruAccountingReport::getEntryAgeValidation);
        add(columns, "ValidacionEdadPermanencia", PeruAccountingReport::getPermanenceAgeValidation);
        add(columns, "ValidacionCarencia", PeruAccountingReport::getWaitingPeriodValidation);
        add(columns, "FechaOcurrencia", PeruAccountingReport::getOccurrenceDate);
        add(columns, "MesOcurrencia", PeruAccountingReport::getOccurrenceMonth);
        add(columns, "TipoDocAsegurado", PeruAccountingReport::getInsuredDocumentType);
        add(columns, "NroDocAsegurado", PeruAccountingReport::getInsuredDocumentNumber);
    }

    private static void addColumnsThree(List<ExcelColumn> columns) {
        add(columns, "NombreAsegurado", PeruAccountingReport::getInsuredName);
        add(columns, "ControlDuplicidad", PeruAccountingReport::getDuplicationControl);
        add(columns, "Genero", PeruAccountingReport::getGender);
        add(columns, "Nacionalidad", PeruAccountingReport::getNationality);
        add(columns, "FechaNacto", PeruAccountingReport::getBirthDate);
        add(columns, "EdadFecOcurrencia", PeruAccountingReport::getAgeAtOccurrenceDate);
        add(columns, "CoberturaAfectada", PeruAccountingReport::getAffectedCoverage);
        add(columns, "Moneda", PeruAccountingReport::getCurrency);
        add(columns, "ReservaInicial", PeruAccountingReport::getInitialReserve);
        add(columns, "PagoReal", PeruAccountingReport::getActualPayment);
    }

    private static void addColumnsFour(List<ExcelColumn> columns) {
        add(columns, "SaldoReserva", PeruAccountingReport::getReserveBalance);
        add(columns, "EstadoSiniestro2", PeruAccountingReport::getClaimStatus);
        add(columns, "EstadoMayor", PeruAccountingReport::getMajorStatus);
        add(columns, "FechaRegTransaccion", PeruAccountingReport::getTransactionRegistrationDate);
        add(columns, "MesAprobacionRechazo", PeruAccountingReport::getApprovalRejectionMonth);
        add(columns, "Cie10", PeruAccountingReport::getCie10);
        add(columns, "Diagnostico", PeruAccountingReport::getDiagnosis);
        add(columns, "MotivoRechazo", PeruAccountingReport::getRejectionReason);
        add(columns, "MotivoRechazoAgrupado", PeruAccountingReport::getGroupedRejectionReason);
        add(columns, "NroPlanilla", PeruAccountingReport::getPayrollNumber);
    }

    private static void addColumnsFive(List<ExcelColumn> columns) {
        add(columns, "NroCarta", PeruAccountingReport::getLetterNumber);
        add(columns, "Observaciones", PeruAccountingReport::getObservations);
        add(columns, "Resumen", PeruAccountingReport::getSummary);
        add(columns, "Ubicacion", PeruAccountingReport::getLocation);
        add(columns, "FechaEntregaLiquiContab", PeruAccountingReport::getAccountingSettlementDeliveryDate);
        add(columns, "FechaEmiCheque", PeruAccountingReport::getCheckIssueDate);
        add(columns, "FechaEntrCheque", PeruAccountingReport::getCheckDeliveryDate);
        add(columns, "ValorMaxCuota", PeruAccountingReport::getMaximumInstallmentValue);
        add(columns, "NumeroCuota", PeruAccountingReport::getInstallmentNumber);
        add(columns, "Plan1", PeruAccountingReport::getPlanOne);
    }

    private static void addColumnsSix(List<ExcelColumn> columns) {
        add(columns, "EjecutivoCAFAE", PeruAccountingReport::getCafaeExecutive);
        add(columns, "RefCAFAE", PeruAccountingReport::getCafaeReference);
        add(columns, "Parentesco", PeruAccountingReport::getRelationship);
        add(columns, "Contrato/Expediente", PeruAccountingReport::getContractOrFile);
        add(columns, "EjecutivoCAFAE2", PeruAccountingReport::getSecondaryCafaeExecutive);
        add(columns, "Parentesco1", PeruAccountingReport::getSecondaryRelationship);
        add(columns, "Plan2", PeruAccountingReport::getPlanTwo);
        add(columns, "TipoDocBeneficiario", PeruAccountingReport::getBeneficiaryDocumentType);
        add(columns, "NroDocBeneficiario", PeruAccountingReport::getBeneficiaryDocumentNumber);
        add(columns, "Parentesco2", PeruAccountingReport::getBeneficiaryRelationship);
    }

    private static void addColumnsSeven(List<ExcelColumn> columns) {
        add(columns, "FondoCAFAE", PeruAccountingReport::getCafaeFund);
        add(columns, "DiasCN", PeruAccountingReport::getCnDays);
        add(columns, "DiasUCI", PeruAccountingReport::getIntensiveCareDays);
        add(columns, "CalculoLiquidacion", PeruAccountingReport::getSettlementCalculation);
        add(columns, "SucursalRetiro", PeruAccountingReport::getWithdrawalBranch);
        add(columns, "Celular", PeruAccountingReport::getMobilePhone);
        add(columns, "Cartera", PeruAccountingReport::getWallet);
        add(columns, "Maletin", PeruAccountingReport::getBriefcase);
        add(columns, "Billetera", PeruAccountingReport::getBillfold);
        add(columns, "PortaDcmtos", PeruAccountingReport::getDocumentHolder);
    }

    private static void addColumnsEight(List<ExcelColumn> columns) {
        add(columns, "LentesOpticos", PeruAccountingReport::getOpticalGlasses);
        add(columns, "LentesSol", PeruAccountingReport::getSunglasses);
        add(columns, "Cosmeticos", PeruAccountingReport::getCosmetics);
        add(columns, "Lapicero", PeruAccountingReport::getPen);
        add(columns, "DNI", PeruAccountingReport::getNationalIdentityDocument);
        add(columns, "Mochila", PeruAccountingReport::getBackpack);
        add(columns, "Reloj", PeruAccountingReport::getWatch);
        add(columns, "DiscIpodMP3Tablet", PeruAccountingReport::getElectronicDevices);
        add(columns, "PalmTablet", PeruAccountingReport::getPalmTablet);
        add(columns, "Bolso", PeruAccountingReport::getBag);
    }

    private static void addColumnsNine(List<ExcelColumn> columns) {
        add(columns, "SillaAutoBB", PeruAccountingReport::getBabyCarSeat);
        add(columns, "CocheBB", PeruAccountingReport::getBabyStroller);
        add(columns, "Discos", PeruAccountingReport::getDiscs);
        add(columns, "Llanta", PeruAccountingReport::getTire);
        add(columns, "GasMedicos", PeruAccountingReport::getMedicalGases);
        add(columns, "LibreDispon", PeruAccountingReport::getFreeAvailability);
        add(columns, "MuerteAccid", PeruAccountingReport::getAccidentalDeath);
        add(columns, "Llaves", PeruAccountingReport::getKeys);
        add(columns, "DiasHospitalizacion", PeruAccountingReport::getHospitalizationDays);
        add(columns, "Excepción", PeruAccountingReport::getException);
    }

    private static void addColumnsTen(List<ExcelColumn> columns) {
        add(columns, "TelefonoReferencia", PeruAccountingReport::getReferencePhone);
        add(columns, "Contacto", PeruAccountingReport::getContact);
        add(columns, "Correo", PeruAccountingReport::getEmail);
        add(columns, "Direccion", PeruAccountingReport::getAddress);
        add(columns, "Departamento", PeruAccountingReport::getDepartment);
        add(columns, "Provincia", PeruAccountingReport::getProvince);
        add(columns, "Distrito", PeruAccountingReport::getDistrict);
        add(columns, "CodigoRamo", PeruAccountingReport::getBranchCode);
        add(columns, "NroTarjeta", PeruAccountingReport::getCardNumber);
        add(columns, "TipoTarjeta", PeruAccountingReport::getCardType);
    }

    private static void addColumnsEleven(List<ExcelColumn> columns) {
        add(columns, "ReasegurosPenCAFAE", PeruAccountingReport::getCafaePendingReinsurance);
        add(columns, "SaldoReservaCoaseguroReaseguros", PeruAccountingReport::getCoinsuranceReinsuranceReserveBalance);
        add(columns, "SaldoReservaCoaseguroReaseguroRECH", PeruAccountingReport::getRejectedCoinsuranceReinsuranceReserveBalance);
        add(columns, "CodigoAct", PeruAccountingReport::getActivityCode);
        add(columns, "TasaRechazo", PeruAccountingReport::getRejectionRate);
        add(columns, "SaldoReservaTasaRechazo", PeruAccountingReport::getRejectionRateReserveBalance);
        add(columns, "FechaReporte", PeruAccountingReport::getReportDate);
        add(columns, "Pandemia", PeruAccountingReport::getPandemic);
        add(columns, "Fechamovimiento2", PeruAccountingReportExcelHelper::getMovementDate);
        add(columns, "FamiliaCobertura", PeruAccountingReport::getCoverageFamily);
    }

    private static void addColumnsTwelve(List<ExcelColumn> columns) {
        add(columns, "FechaEnvioCartas", PeruAccountingReport::getLetterSentDate);
        add(columns, "DiasIngresos", PeruAccountingReport::getEntryDays);
        add(columns, "RangoIngresos", PeruAccountingReport::getEntryRange);
        add(columns, "DiasTrascurridosAvisosocio", PeruAccountingReport::getPartnerNoticeElapsedDays);
        add(columns, "DiasTrascurridosAvisocardif", PeruAccountingReport::getCardifNoticeElapsedDays);
        add(columns, "RangoAvisosocios", PeruAccountingReport::getPartnerNoticeRange);
        add(columns, "RangoAvisocardif", PeruAccountingReport::getCardifNoticeRange);
        add(columns, "CanalIngreso", PeruAccountingReport::getEntryChannel);
        add(columns, "RamoProductos", PeruAccountingReport::getProductBranch);
        add(columns, "Causalobjecion_scoring", PeruAccountingReport::getScoringObjectionReason);
    }

    private static void add(
            List<ExcelColumn> columns,
            String header,
            Function<PeruAccountingReport, Object> extractor) {

        columns.add(new ExcelColumn(header, extractor));
    }

    private static String getClaimNumber(
            PeruAccountingReport report) {

        return report.getId() == null
                ? null
                : report.getId().getClaimNumber();
    }

    private static LocalDateTime getMovementDate(
            PeruAccountingReport report) {

        return report.getId() == null
                ? null
                : report.getId().getMovementDate();
    }

    /**
     * Define el encabezado y la función encargada de obtener cada valor.
     */
    private static final class ExcelColumn {

        private final String header;
        private final Function<PeruAccountingReport, Object> extractor;

        private ExcelColumn(
                String header,
                Function<PeruAccountingReport, Object> extractor) {

            this.header = header;
            this.extractor = extractor;
        }

        private String getHeader() {
            return header;
        }

        private Object getValue(PeruAccountingReport report) {
            return extractor.apply(report);
        }
    }
}
