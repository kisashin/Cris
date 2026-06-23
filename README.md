package co.com.bnpparibas.cardif.closingclaims.domain.util.helpers;

import co.com.bnpparibas.cardif.closingclaims.domain.entity.CardifPeruClosing;
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
 * Helper que genera el archivo Excel del reporte de movimientos Cardif Perú.
 *
 * <p>Todas las celdas se escriben como TEXTO. La vista contiene identificadores
 * que se corromperían como número: {@code NumeroSiniestro} es alfanumérico,
 * {@code Certificado} llega a 17 dígitos (Excel solo conserva 15 cifras
 * significativas) y {@code NumeroSiniestro}/{@code CodPlan} pueden traer ceros
 * a la izquierda. Esto replica el comportamiento del legacy, que forzaba texto
 * con {@code mso-number-format:\@}.</p>
 *
 * <p>Los tres valores monetarios ({@code Valordeuda}, {@code Valoraseguradototal},
 * {@code Vrmovimiento}) son {@code float} en base de datos; se formatean con
 * {@link BigDecimal} (inmutable, seguro para concurrencia) para evitar ruido
 * binario del {@code float} y para no usar conversiones genéricas tipo
 * {@code String.valueOf(value)}.</p>
 */
@Component
public class CardifPeruClosingExcelHelper {

    private static final String SHEET_NAME = "Movimientos Cardif Peru";
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
    public byte[] generateExcel(List<CardifPeruClosing> movements)
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
            List<CardifPeruClosing> movements) throws IOException {

        try (ByteArrayOutputStream outputStream =
                     new ByteArrayOutputStream()) {

            populateWorkbook(workbook, movements);
            workbook.write(outputStream);
            return outputStream.toByteArray();
        }
    }

    private void populateWorkbook(
            SXSSFWorkbook workbook,
            List<CardifPeruClosing> movements) {

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
            List<CardifPeruClosing> movements) {

        int rowIndex = 1;

        for (CardifPeruClosing movement : movements) {
            createDataRow(sheet.createRow(rowIndex++), movement);
        }
    }

    private void createDataRow(
            Row row,
            CardifPeruClosing movement) {

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

        if (value instanceof Double) {
            cell.setCellValue(formatMoney((Double) value));
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

    private String formatMoney(Double value) {
        return BigDecimal.valueOf(value)
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
        add(columns, "IDCARVAJAL", CardifPeruClosing::getIdCarvajal);
        add(columns, "Socio", CardifPeruClosing::getPartner);
        add(columns, "NumeroSiniestro", CardifPeruClosing::getClaimNumber);
        add(columns, "Nroidentificacion", CardifPeruClosing::getIdentificationNumber);
        add(columns, "Tipodocumento", CardifPeruClosing::getDocumentType);
        add(columns, "Fechanacimiento", CardifPeruClosing::getBirthDate);
        add(columns, "Genero", CardifPeruClosing::getGender);
        add(columns, "Direccion", CardifPeruClosing::getAddress);
        add(columns, "Ciudad", CardifPeruClosing::getCity);
    }

    private static void addColumnsTwo(List<ExcelColumn> columns) {
        add(columns, "Telefono", CardifPeruClosing::getPhone);
        add(columns, "Celular", CardifPeruClosing::getMobilePhone);
        add(columns, "Actividad", CardifPeruClosing::getActivity);
        add(columns, "Nomproducto", CardifPeruClosing::getProductName);
        add(columns, "Codproducto", CardifPeruClosing::getProductCode);
        add(columns, "CodPlan", CardifPeruClosing::getPlanCode);
        add(columns, "Cobertura", CardifPeruClosing::getCoverage);
        add(columns, "Ramo", CardifPeruClosing::getBranch);
        add(columns, "Cuotasapagar", CardifPeruClosing::getInstallmentsToPay);
    }

    private static void addColumnsThree(List<ExcelColumn> columns) {
        add(columns, "Certificado", CardifPeruClosing::getCertificate);
        add(columns, "Fechainiciovigencia", CardifPeruClosing::getPolicyStartDate);
        add(columns, "Fechaocurrencia", CardifPeruClosing::getOccurrenceDate);
        add(columns, "Fechaavisosocio", CardifPeruClosing::getPartnerNoticeDate);
        add(columns, "Fechaavisocardif", CardifPeruClosing::getCardifNoticeDate);
        add(columns, "Valordeuda", CardifPeruClosing::getDebtValue);
        add(columns, "Valoraseguradototal", CardifPeruClosing::getTotalInsuredValue);
        add(columns, "Fechasistematizacion", CardifPeruClosing::getSystematizationDate);
        add(columns, "Fecharecepmiddle", CardifPeruClosing::getMiddleReceptionDate);
    }

    private static void addColumnsFour(List<ExcelColumn> columns) {
        add(columns, "Fecharecepback", CardifPeruClosing::getBackReceptionDate);
        add(columns, "Fechaconfcartera", CardifPeruClosing::getPortfolioConfirmationDate);
        add(columns, "Causaobjecion", CardifPeruClosing::getObjectionReason);
        add(columns, "Fechaenviocartaobj", CardifPeruClosing::getObjectionLetterSentDate);
        add(columns, "Causalsuspenso", CardifPeruClosing::getSuspenseReason);
        add(columns, "Fechamovimiento", CardifPeruClosing::getMovementDate);
        add(columns, "Vrmovimiento", CardifPeruClosing::getMovementValue);
        add(columns, "Beneficiariopago", CardifPeruClosing::getPaymentBeneficiary);
        add(columns, "Pagocomercial", CardifPeruClosing::getCommercialPayment);
    }

    private static void addColumnsFive(List<ExcelColumn> columns) {
        add(columns, "Fechaentregaultdocto", CardifPeruClosing::getLastDocumentDeliveryDate);
        add(columns, "Iddoctosoportemanutencion", CardifPeruClosing::getMaintenanceSupportDocumentId);
        add(columns, "Codsocio", CardifPeruClosing::getPartnerCode);
        add(columns, "Analista", CardifPeruClosing::getAnalyst);
        add(columns, "Nopoliza", CardifPeruClosing::getPolicyNumber);
        add(columns, "Idcardif", CardifPeruClosing::getCardifId);
        add(columns, "Llavesiniestro", CardifPeruClosing::getClaimKey);
        add(columns, "Nombreasegurado", CardifPeruClosing::getInsuredName);
        add(columns, "Edad", CardifPeruClosing::getAge);
    }

    private static void addColumnsSix(List<ExcelColumn> columns) {
        add(columns, "Estadosiniestro", CardifPeruClosing::getClaimStatus);
        add(columns, "Estadomayor", CardifPeruClosing::getMajorStatus);
        add(columns, "Fechaestadosiniestro", CardifPeruClosing::getClaimStatusDate);
        add(columns, "Tipomovimiento", CardifPeruClosing::getMovementType);
        add(columns, "Conceptopago", CardifPeruClosing::getPaymentConcept);
        add(columns, "Informacion", CardifPeruClosing::getInformation);
        add(columns, "Baseorigen", CardifPeruClosing::getSourceBase);
        add(columns, "Anomovimiento", CardifPeruClosing::getMovementYear);
        add(columns, "Mesmovimiento", CardifPeruClosing::getMovementMonth);
    }

    private static void addColumnsSeven(List<ExcelColumn> columns) {
        add(columns, "Diamovimiento", CardifPeruClosing::getMovementDay);
        add(columns, "Anomessist", CardifPeruClosing::getSystemYearMonth);
        add(columns, "Anosist", CardifPeruClosing::getSystemYear);
        add(columns, "Messist", CardifPeruClosing::getSystemMonth);
        add(columns, "Agrupacionmov", CardifPeruClosing::getMovementGrouping);
        add(columns, "Tipopago", CardifPeruClosing::getPaymentType);
        add(columns, "Fechadesembolso", CardifPeruClosing::getDisbursementDate);
        add(columns, "Clasepago", CardifPeruClosing::getPaymentClass);
        add(columns, "Estadopagoprog", CardifPeruClosing::getScheduledPaymentStatus);
    }

    private static void addColumnsEight(List<ExcelColumn> columns) {
        add(columns, "Vrcuotaplan", CardifPeruClosing::getPlanInstallmentValue);
        add(columns, "Estadosiniestro2", CardifPeruClosing::getClaimStatusTwo);
        add(columns, "Estadomayor2", CardifPeruClosing::getMajorStatusTwo);
        add(columns, "Fechaestadosiniestro2", CardifPeruClosing::getClaimStatusDateTwo);
        add(columns, "Fechaentregaultdocto2", CardifPeruClosing::getLastDocumentDeliveryDateTwo);
        add(columns, "Fechamovimiento2", CardifPeruClosing::getMovementDateTwo);
        add(columns, "Fechacontabilizacion", CardifPeruClosing::getAccountingDate);
        add(columns, "vrReaseguroRetenido", CardifPeruClosing::getRetainedReinsuranceValue);
        add(columns, "Moneda", CardifPeruClosing::getCurrency);
    }

    private static void add(
            List<ExcelColumn> columns,
            String header,
            Function<CardifPeruClosing, Object> extractor) {

        columns.add(new ExcelColumn(header, extractor));
    }

    /**
     * Define el encabezado y la función encargada de obtener cada valor.
     */
    private static final class ExcelColumn {

        private final String header;
        private final Function<CardifPeruClosing, Object> extractor;

        private ExcelColumn(
                String header,
                Function<CardifPeruClosing, Object> extractor) {

            this.header = header;
            this.extractor = extractor;
        }

        private String getHeader() {
            return header;
        }

        private Object getValue(CardifPeruClosing movement) {
            return extractor.apply(movement);
        }
    }
}
