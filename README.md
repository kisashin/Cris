CardifCenterClosingExcelHelper

package co.com.bnpparibas.cardif.closingclaims.domain.util.helpers;

import co.com.bnpparibas.cardif.closingclaims.domain.entity.CardifCenterClosing;
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
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.function.Function;

/**
 * Helper que genera el archivo Excel del reporte de movimientos Cardif Centroamérica.
 *
 * <p>Todas las celdas se escriben como TEXTO. La vista contiene identificadores
 * que se corromperían como número: {@code NumeroSiniestro} es alfanumérico,
 * {@code Certificado} llega a 17 dígitos (Excel solo conserva 15 cifras
 * significativas) y {@code NumeroSiniestro}/{@code CodPlan} pueden traer ceros
 * a la izquierda. Esto replica el comportamiento del legacy, que forzaba texto
 * con {@code mso-number-format:\@}.</p>
 *
 * <p>Los valores monetarios se formatean con {@link BigDecimal} (inmutable,
 * seguro para concurrencia) y {@code setScale(2)}, evitando conversiones
 * genéricas tipo {@code String.valueOf(value)}. {@code Valordeuda} y
 * {@code Valoraseguradototal} son {@code float} ({@code Double});
 * {@code Vrmovimiento} es {@code decimal(38,2)} ({@code BigDecimal}).</p>
 */
@Component
public class CardifCenterClosingExcelHelper {

    private static final String SHEET_NAME = "Movimientos Cardif Centro";
    private static final int ROW_ACCESS_WINDOW_SIZE = 100;
    private static final int MINIMUM_COLUMN_WIDTH = 15;
    private static final int MAXIMUM_COLUMN_WIDTH = 40;
    private static final int MONEY_SCALE = 2;

    private static final List<ExcelColumn> COLUMNS = createColumns();

    /**
     * Genera el archivo Excel con la información de movimientos.
     *
     * @param movements registros que serán exportados.
     * @return contenido binario del archivo Excel.
     * @throws IOException cuando no es posible generar el archivo.
     */
    public byte[] generateExcel(List<CardifCenterClosing> movements)
            throws IOException {

        SXSSFWorkbook workbook = createWorkbook();

        try {
            return writeWorkbook(workbook, movements);
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
            List<CardifCenterClosing> movements) throws IOException {

        try (ByteArrayOutputStream outputStream =
                     new ByteArrayOutputStream()) {

            populateWorkbook(workbook, movements);
            workbook.write(outputStream);
            return outputStream.toByteArray();
        }
    }

    private void populateWorkbook(
            SXSSFWorkbook workbook,
            List<CardifCenterClosing> movements) {

        Sheet sheet = workbook.createSheet(SHEET_NAME);
        CellStyle headerStyle = createHeaderStyle(workbook);

        createHeaderRow(sheet, headerStyle);
        createDataRows(sheet, movements);
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
            List<CardifCenterClosing> movements) {

        int rowIndex = 1;

        for (CardifCenterClosing movement : movements) {
            createDataRow(sheet.createRow(rowIndex++), movement);
        }
    }

    private void createDataRow(
            Row row,
            CardifCenterClosing movement) {

        for (int index = 0; index < COLUMNS.size(); index++) {
            Object value = COLUMNS.get(index).getValue(movement);
            writeCell(row.createCell(index), value);
        }
    }

    /**
     * Escribe cada celda como texto, despachando por tipo. El mensaje de error
     * solo expone el tipo de dato, nunca el valor, para no filtrar información
     * sensible.
     */
    private void writeCell(Cell cell, Object value) {

        if (value == null) {
            cell.setBlank();
            return;
        }

        if (value instanceof String) {
            cell.setCellValue((String) value);
            return;
        }

        if (value instanceof BigDecimal) {
            cell.setCellValue(formatMoney((BigDecimal) value));
            return;
        }

        if (value instanceof Double) {
            cell.setCellValue(formatMoney(BigDecimal.valueOf((Double) value)));
            return;
        }

        if (value instanceof Integer) {
            cell.setCellValue(Integer.toString((Integer) value));
            return;
        }

        if (value instanceof Long) {
            cell.setCellValue(Long.toString((Long) value));
            return;
        }

        throw new IllegalArgumentException(
                "Unsupported Excel cell value type: "
                        + value.getClass().getName());
    }

    private String formatMoney(BigDecimal value) {
        return value
                .setScale(MONEY_SCALE, RoundingMode.HALF_UP)
                .toPlainString();
    }

    private void configureSheet(Sheet sheet) {
        sheet.createFreezePane(0, 1);
        sheet.setAutoFilter(
                new CellRangeAddress(0, 0, 0, COLUMNS.size() - 1));

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

        return Collections.unmodifiableList(columns);
    }

    private static void addColumnsOne(List<ExcelColumn> columns) {
        add(columns, "IDCARVAJAL", CardifCenterClosing::getIdCarvajal);
        add(columns, "Socio", CardifCenterClosing::getPartner);
        add(columns, "NumeroSiniestro", CardifCenterClosing::getClaimNumber);
        add(columns, "Nroidentificacion", CardifCenterClosing::getIdentificationNumber);
        add(columns, "Tipodocumento", CardifCenterClosing::getDocumentType);
        add(columns, "Fechanacimiento", CardifCenterClosing::getBirthDate);
        add(columns, "Genero", CardifCenterClosing::getGender);
        add(columns, "Direccion", CardifCenterClosing::getAddress);
        add(columns, "Ciudad", CardifCenterClosing::getCity);
    }

    private static void addColumnsTwo(List<ExcelColumn> columns) {
        add(columns, "Telefono", CardifCenterClosing::getPhone);
        add(columns, "Celular", CardifCenterClosing::getMobilePhone);
        add(columns, "Actividad", CardifCenterClosing::getActivity);
        add(columns, "Nomproducto", CardifCenterClosing::getProductName);
        add(columns, "Codproducto", CardifCenterClosing::getProductCode);
        add(columns, "CodPlan", CardifCenterClosing::getPlanCode);
        add(columns, "Cobertura", CardifCenterClosing::getCoverage);
        add(columns, "Ramo", CardifCenterClosing::getBranch);
        add(columns, "Cuotasapagar", CardifCenterClosing::getInstallmentsToPay);
    }

    private static void addColumnsThree(List<ExcelColumn> columns) {
        add(columns, "Certificado", CardifCenterClosing::getCertificate);
        add(columns, "Fechainiciovigencia", CardifCenterClosing::getPolicyStartDate);
        add(columns, "Fechaocurrencia", CardifCenterClosing::getOccurrenceDate);
        add(columns, "Fechaavisosocio", CardifCenterClosing::getPartnerNoticeDate);
        add(columns, "Fechaavisocardif", CardifCenterClosing::getCardifNoticeDate);
        add(columns, "Valordeuda", CardifCenterClosing::getDebtValue);
        add(columns, "Valoraseguradototal", CardifCenterClosing::getTotalInsuredValue);
        add(columns, "Fechasistematizacion", CardifCenterClosing::getSystematizationDate);
        add(columns, "Fecharecepmiddle", CardifCenterClosing::getMiddleReceptionDate);
    }

    private static void addColumnsFour(List<ExcelColumn> columns) {
        add(columns, "Fecharecepback", CardifCenterClosing::getBackReceptionDate);
        add(columns, "Fechaconfcartera", CardifCenterClosing::getPortfolioConfirmationDate);
        add(columns, "Causaobjecion", CardifCenterClosing::getObjectionReason);
        add(columns, "Fechaenviocartaobj", CardifCenterClosing::getObjectionLetterSentDate);
        add(columns, "Causalsuspenso", CardifCenterClosing::getSuspenseReason);
        add(columns, "Fechamovimiento", CardifCenterClosing::getMovementDate);
        add(columns, "Vrmovimiento", CardifCenterClosing::getMovementValue);
        add(columns, "Beneficiariopago", CardifCenterClosing::getPaymentBeneficiary);
        add(columns, "Pagocomercial", CardifCenterClosing::getCommercialPayment);
    }

    private static void addColumnsFive(List<ExcelColumn> columns) {
        add(columns, "Fechaentregaultdocto", CardifCenterClosing::getLastDocumentDeliveryDate);
        add(columns, "Iddoctosoportemanutencion", CardifCenterClosing::getMaintenanceSupportDocumentId);
        add(columns, "Codsocio", CardifCenterClosing::getPartnerCode);
        add(columns, "Analista", CardifCenterClosing::getAnalyst);
        add(columns, "Nopoliza", CardifCenterClosing::getPolicyNumber);
        add(columns, "Idcardif", CardifCenterClosing::getCardifId);
        add(columns, "Llavesiniestro", CardifCenterClosing::getClaimKey);
        add(columns, "Nombreasegurado", CardifCenterClosing::getInsuredName);
        add(columns, "Edad", CardifCenterClosing::getAge);
    }

    private static void addColumnsSix(List<ExcelColumn> columns) {
        add(columns, "Estadosiniestro", CardifCenterClosing::getClaimStatus);
        add(columns, "Estadomayor", CardifCenterClosing::getMajorStatus);
        add(columns, "Fechaestadosiniestro", CardifCenterClosing::getClaimStatusDate);
        add(columns, "Tipomovimiento", CardifCenterClosing::getMovementType);
        add(columns, "Conceptopago", CardifCenterClosing::getPaymentConcept);
        add(columns, "Informacion", CardifCenterClosing::getInformation);
        add(columns, "Baseorigen", CardifCenterClosing::getSourceBase);
        add(columns, "Anomovimiento", CardifCenterClosing::getMovementYear);
        add(columns, "Mesmovimiento", CardifCenterClosing::getMovementMonth);
    }

    private static void addColumnsSeven(List<ExcelColumn> columns) {
        add(columns, "Diamovimiento", CardifCenterClosing::getMovementDay);
        add(columns, "Anomessist", CardifCenterClosing::getSystemYearMonth);
        add(columns, "Anosist", CardifCenterClosing::getSystemYear);
        add(columns, "Messist", CardifCenterClosing::getSystemMonth);
        add(columns, "Agrupacionmov", CardifCenterClosing::getMovementGrouping);
        add(columns, "Tipopago", CardifCenterClosing::getPaymentType);
        add(columns, "Fechadesembolso", CardifCenterClosing::getDisbursementDate);
        add(columns, "Clasepago", CardifCenterClosing::getPaymentClass);
        add(columns, "Estadopagoprog", CardifCenterClosing::getScheduledPaymentStatus);
    }

    private static void addColumnsEight(List<ExcelColumn> columns) {
        add(columns, "Vrcuotaplan", CardifCenterClosing::getPlanInstallmentValue);
        add(columns, "Estadosiniestro2", CardifCenterClosing::getClaimStatusTwo);
        add(columns, "Estadomayor2", CardifCenterClosing::getMajorStatusTwo);
        add(columns, "Fechaestadosiniestro2", CardifCenterClosing::getClaimStatusDateTwo);
        add(columns, "Fechaentregaultdocto2", CardifCenterClosing::getLastDocumentDeliveryDateTwo);
        add(columns, "Fechamovimiento2", CardifCenterClosing::getMovementDateTwo);
        add(columns, "Fechacontabilizacion", CardifCenterClosing::getAccountingDate);
        add(columns, "vrReaseguroRetenido", CardifCenterClosing::getRetainedReinsuranceValue);
        add(columns, "Moneda", CardifCenterClosing::getCurrency);
    }

    private static void add(
            List<ExcelColumn> columns,
            String header,
            Function<CardifCenterClosing, Object> extractor) {

        columns.add(new ExcelColumn(header, extractor));
    }

    /**
     * Define el encabezado y la función encargada de obtener cada valor.
     */
    private static final class ExcelColumn {

        private final String header;
        private final Function<CardifCenterClosing, Object> extractor;

        private ExcelColumn(
                String header,
                Function<CardifCenterClosing, Object> extractor) {

            this.header = header;
            this.extractor = extractor;
        }

        private String getHeader() {
            return header;
        }

        private Object getValue(CardifCenterClosing movement) {
            return extractor.apply(movement);
        }
    }
}
