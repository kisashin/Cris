package co.com.bnpparibas.cardif.closingclaims.domain.util.helpers;

import co.com.bnpparibas.cardif.closingclaims.domain.entity.PeruAccountingReport;
import co.com.bnpparibas.cardif.closingclaims.domain.entity.PeruAccountingReportId;
import org.apache.poi.ss.usermodel.DateUtil;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.ss.usermodel.Workbook;
import org.apache.poi.ss.usermodel.WorkbookFactory;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.time.LocalDateTime;
import java.util.Collections;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

class PeruAccountingReportExcelHelperTest {

    private final PeruAccountingReportExcelHelper helper = new PeruAccountingReportExcelHelper();

    @Test
    @DisplayName("Should generate Excel with headers and report data")
    void shouldGenerateExcelWithHeadersAndReportData() throws IOException {

        LocalDateTime movementDate = LocalDateTime.of(2026, 6, 15, 10, 30);
        LocalDateTime reportDate = LocalDateTime.of(2026, 6, 15, 11, 0);

        PeruAccountingReport report = PeruAccountingReport.builder()
                .id(PeruAccountingReportId.builder()
                        .claimNumber("SIN-001")
                        .movementDate(movementDate)
                        .build())
                .noticeDate("15/06/2026")
                .productCode(123.0)
                .reportDate(reportDate)
                .scoringObjectionReason("Test reason")
                .build();

        byte[] file = helper.generateExcel(Collections.singletonList(report));

        assertNotNull(file);
        assertTrue(file.length > 0);

        File tempFile = File.createTempFile("test-excel", ".xlsx");
        try {
            Files.write(tempFile.toPath(), file);
            try (Workbook workbook = WorkbookFactory.create(tempFile)) {
                Sheet sheet = workbook.getSheet("Reporte Contable Peru");
                assertNotNull(sheet);
                assertEquals(1, sheet.getLastRowNum());

                Row headerRow = sheet.getRow(0);
                Row dataRow = sheet.getRow(1);

                assertEquals(120, headerRow.getPhysicalNumberOfCells());
                assertEquals("FechaAviso", headerRow.getCell(0).getStringCellValue());
                assertEquals("NumeroSiniestro", headerRow.getCell(4).getStringCellValue());
                assertEquals("Fechamovimiento2", headerRow.getCell(108).getStringCellValue());
                assertEquals("Causalobjecion_scoring", headerRow.getCell(119).getStringCellValue());

                assertEquals("15/06/2026", dataRow.getCell(0).getStringCellValue());
                assertEquals("SIN-001", dataRow.getCell(4).getStringCellValue());
                assertEquals(123.0, dataRow.getCell(9).getNumericCellValue());
                assertTrue(DateUtil.isCellDateFormatted(dataRow.getCell(106)));
                assertTrue(DateUtil.isCellDateFormatted(dataRow.getCell(108)));
                assertEquals("Test reason", dataRow.getCell(119).getStringCellValue());
            }
        } finally {
            tempFile.delete();
        }
    }

    @Test
    @DisplayName("Should generate Excel with only headers when report list is empty")
    void shouldGenerateExcelWithOnlyHeadersWhenListIsEmpty() throws IOException {

        byte[] file = helper.generateExcel(Collections.emptyList());

        assertNotNull(file);
        assertTrue(file.length > 0);

        File tempFile = File.createTempFile("test-excel", ".xlsx");
        try {
            Files.write(tempFile.toPath(), file);
            try (Workbook workbook = WorkbookFactory.create(tempFile)) {
                Sheet sheet = workbook.getSheet("Reporte Contable Peru");
                assertNotNull(sheet);
                assertEquals(0, sheet.getLastRowNum());
                assertEquals(120, sheet.getRow(0).getPhysicalNumberOfCells());
            }
        } finally {
            tempFile.delete();
        }
    }
}
