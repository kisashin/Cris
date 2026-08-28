package co.com.bnpparibas.cardif.closingclaims.domain.util.helpers;

import co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia.AvalReportRow;
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
 * Helper que genera el archivo Excel del reporte mensual de Aval.
 *
 * <p>Todas las celdas se escriben como TEXTO, replicando el comportamiento
 * del paquete legacy que convertía cada columna a cadena antes de escribirla
 * en la hoja. Los identificadores como {@code SINIESTRO_LIDER} y
 * {@code nro_credito} se corromperían como número.</p>
 */
@Component
public class AvalReportExcelHelper {

    private static final String SHEET_NAME = "Hoja1";
    private static final int ROW_ACCESS_WINDOW_SIZE = 100;
    private static final int MINIMUM_COLUMN_WIDTH = 15;
    private static final int MAXIMUM_COLUMN_WIDTH = 40;
    private static final int MONEY_SCALE = 2;

    private static final List<ExcelColumn> COLUMNS = createColumns();

    /**
     * Genera el archivo Excel con la información del reporte.
     *
     * @param rows registros que serán exportados.
     * @return contenido binario del archivo Excel.
     * @throws IOException cuando no es posible generar el archivo.
     */
    public byte[] generateExcel(List<AvalReportRow> rows)
            throws IOException {

        SXSSFWorkbook workbook = createWorkbook();

        try {
            return writeWorkbook(workbook, rows);
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
            List<AvalReportRow> rows) throws IOException {

        try (ByteArrayOutputStream outputStream =
                     new ByteArrayOutputStream()) {

            populateWorkbook(workbook, rows);
            workbook.write(outputStream);
            return outputStream.toByteArray();
        }
    }

    private void populateWorkbook(
            SXSSFWorkbook workbook,
            List<AvalReportRow> rows) {

        Sheet sheet = workbook.createSheet(SHEET_NAME);
        CellStyle headerStyle = createHeaderStyle(workbook);

        createHeaderRow(sheet, headerStyle);
        createDataRows(sheet, rows);
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
            List<AvalReportRow> rows) {

        int rowIndex = 1;

        for (AvalReportRow row : rows) {
            createDataRow(sheet.createRow(rowIndex++), row);
        }
    }

    private void createDataRow(
            Row excelRow,
            AvalReportRow reportRow) {

        for (int index = 0; index < COLUMNS.size(); index++) {
            Object value = COLUMNS.get(index).getValue(reportRow);
            writeCell(excelRow.createCell(index), value);
        }
    }

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

        return Collections.unmodifiableList(columns);
    }

    private static void addColumnsOne(List<ExcelColumn> columns) {
        add(columns, "compania", AvalReportRow::getCompania);
        add(columns, "sucursal", AvalReportRow::getSucursal);
        add(columns, "descripcion_ramo", AvalReportRow::getDescripcionRamo);
        add(columns, "symbol", AvalReportRow::getSymbol);
        add(columns, "ramo2", AvalReportRow::getRamo2);
        add(columns, "nro_poliza", AvalReportRow::getNroPoliza);
        add(columns, "modulo", AvalReportRow::getModulo);
        add(columns, "cod_banco_negocio", AvalReportRow::getCodBancoNegocio);
        add(columns, "DESCRIPCION_TOMADOR",
                AvalReportRow::getDescripcionTomador);
    }

    private static void addColumnsTwo(List<ExcelColumn> columns) {
        add(columns, "poliza_lider_alfa", AvalReportRow::getPolizaLiderAlfa);
        add(columns, "SINIESTRO_LIDER", AvalReportRow::getSiniestroLider);
        add(columns, "valor", AvalReportRow::getValor);
        add(columns, "NUMERO_LOTE", AvalReportRow::getNumeroLote);
        add(columns, "CAMPO_UNION", AvalReportRow::getCampoUnion);
        add(columns, "VALOR_INICIAL_RESERVA",
                AvalReportRow::getValorInicialReserva);
        add(columns, "VALOR_AJUSTES_RESERVA",
                AvalReportRow::getValorAjustesReserva);
        add(columns, "VALOR_PAGOS", AvalReportRow::getValorPagos);
        add(columns, "VALOR_ACTUAL_RESERVA",
                AvalReportRow::getValorActualReserva);
    }

    private static void addColumnsThree(List<ExcelColumn> columns) {
        add(columns, "PORCENTAJE_ALFA", AvalReportRow::getPorcentajeAlfa);
        add(columns, "VALOR_GASTOS_COASEGURO",
                AvalReportRow::getValorGastosCoaseguro);
        add(columns, "VALOR_SALVAMENTO", AvalReportRow::getValorSalvamento);
        add(columns, "VALOR_RECUPERACIONES",
                AvalReportRow::getValorRecuperaciones);
        add(columns, "Nroidentificacion",
                AvalReportRow::getNroidentificacion);
        add(columns, "Nombreasegurado", AvalReportRow::getNombreasegurado);
        add(columns, "fechanacimiento", AvalReportRow::getFechanacimiento);
        add(columns, "edad", AvalReportRow::getEdad);
        add(columns, "SEXO", AvalReportRow::getSexo);
    }

    private static void addColumnsFour(List<ExcelColumn> columns) {
        add(columns, "Profesion", AvalReportRow::getProfesion);
        add(columns, "fechaperdida", AvalReportRow::getFechaperdida);
        add(columns, "fechaaviso", AvalReportRow::getFechaaviso);
        add(columns, "fechareclamo", AvalReportRow::getFechareclamo);
        add(columns, "CODIGO_CAUSA", AvalReportRow::getCodigoCausa);
        add(columns, "causa_siniestro", AvalReportRow::getCausaSiniestro);
        add(columns, "ciudad", AvalReportRow::getCiudad);
        add(columns, "Tipo_siniestro", AvalReportRow::getTipoSiniestro);
        add(columns, "nro_credito", AvalReportRow::getNroCredito);
    }

    private static void addColumnsFive(List<ExcelColumn> columns) {
        add(columns, "fechadesembolso", AvalReportRow::getFechadesembolso);
        add(columns, "porcentaje_asegurabilidad",
                AvalReportRow::getPorcentajeAsegurabilidad);
        add(columns, "tipocredito", AvalReportRow::getTipocredito);
        add(columns, "cobertura_lider", AvalReportRow::getCoberturaLider);
        add(columns, "reportado_por", AvalReportRow::getReportadoPor);
        add(columns, "Nit_beneficiario",
                AvalReportRow::getNitBeneficiario);
        add(columns, "Beneficiario", AvalReportRow::getBeneficiario);
        add(columns, "causal_objecion", AvalReportRow::getCausalObjecion);
        add(columns, "fecha_objecion", AvalReportRow::getFechaObjecion);
    }

    private static void addColumnsSix(List<ExcelColumn> columns) {
        add(columns, "PLACA_", AvalReportRow::getPlaca);
        add(columns, "SERIAL_", AvalReportRow::getSerial);
        add(columns, "MOTOR_", AvalReportRow::getMotor);
        add(columns, "TIPO_VEHICULO", AvalReportRow::getTipoVehiculo);
        add(columns, "CLASE_VEHICULO", AvalReportRow::getClaseVehiculo);
        add(columns, "OBSERVACIONES_PAGO",
                AvalReportRow::getObservacionesPago);
    }

    private static void add(
            List<ExcelColumn> columns,
            String header,
            Function<AvalReportRow, Object> extractor) {

        columns.add(new ExcelColumn(header, extractor));
    }

    /**
     * Define el encabezado y la función encargada de obtener cada valor.
     */
    private static final class ExcelColumn {

        private final String header;
        private final Function<AvalReportRow, Object> extractor;

        private ExcelColumn(
                String header,
                Function<AvalReportRow, Object> extractor) {

            this.header = header;
            this.extractor = extractor;
        }

        private String getHeader() {
            return header;
        }

        private Object getValue(AvalReportRow row) {
            return extractor.apply(row);
        }
    }
}
