package co.com.bnpparibas.cardif.closingclaims.domain.util.helpers;

import co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia.ColombiaAccountingLine;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia.ColombiaXmlFile;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ColombiaAccountingXmlHelperTest {

    private static final String PERIOD = "202608";

    private final ColombiaAccountingXmlHelper helper =
            new ColombiaAccountingXmlHelper();

    @Test
    @DisplayName("Should return an empty list when there are no lines")
    void shouldReturnEmptyListWhenNoLines() {
        assertTrue(helper.buildFiles(null).isEmpty());
        assertTrue(helper.buildFiles(Collections.emptyList()).isEmpty());
    }

    @Test
    @DisplayName("Should wrap grouped lines with header and footer")
    void shouldWrapGroupedLines() {
        List<ColombiaAccountingLine> lines = Arrays.asList(
                groupedLine("ReasegCardif", 1, "Pago", 1L, "<Line>A</Line>"),
                groupedLine("ReasegCardif", 1, "Pago", 2L, "<Line>B</Line>"));

        List<ColombiaXmlFile> files = helper.buildFiles(lines);

        assertEquals(1, files.size());

        ColombiaXmlFile file = files.get(0);
        assertEquals("ReasegCardif", file.getFamily());
        assertEquals(PERIOD, file.getPeriod());
        assertEquals("Pago", file.getMovementType());
        assertEquals(2, file.getLineCount());
        assertTrue(file.getContent().startsWith("<?xml version=\"1.0\""));
        assertTrue(file.getContent().contains("<Line>A</Line><Line>B</Line>"));
        assertTrue(file.getContent()
                .endsWith("</Ledger></Payload></SSC>"));
    }

    @Test
    @DisplayName("Should split grouped lines by movement type")
    void shouldSplitGroupedLinesByMovementType() {
        List<ColombiaAccountingLine> lines = Arrays.asList(
                groupedLine("ReasegCardif", 1, "Pago", 1L, "<Line>A</Line>"),
                groupedLine("ReasegCardif", 1, "Constitucion", 1L,
                        "<Line>B</Line>"));

        List<ColombiaXmlFile> files = helper.buildFiles(lines);

        assertEquals(2, files.size());
        assertEquals("Constitucion", files.get(0).getMovementType());
        assertEquals("Pago", files.get(1).getMovementType());
    }

    @Test
    @DisplayName("Should split grouped lines by pass")
    void shouldSplitGroupedLinesByPass() {
        List<ColombiaAccountingLine> lines = Arrays.asList(
                groupedLine("ReasegCardif", 1, "Pago", 1L, "<Line>A</Line>"),
                groupedLine("ReasegCardif", 2, "Pago", 1L, "<Line>B</Line>"));

        List<ColombiaXmlFile> files = helper.buildFiles(lines);

        assertEquals(2, files.size());
        assertTrue(files.stream()
                .anyMatch(file -> file.getFileName().startsWith("rv")));
        assertTrue(files.stream()
                .anyMatch(file -> !file.getFileName().startsWith("rv")));
    }

    @Test
    @DisplayName("Should build the file name from the family prefix")
    void shouldBuildFileNameFromFamilyPrefix() {
        String fileDate = LocalDate.now()
                .format(DateTimeFormatter.ofPattern("yyyyMMdd"));

        List<ColombiaXmlFile> files = helper.buildFiles(Arrays.asList(
                groupedLine("ReasegAlfa", 1, "Constitucion", 1L,
                        "<Line>A</Line>"),
                groupedLine("CoaseguroCedido", 1, "Liberacion", 1L,
                        "<Line>B</Line>"),
                groupedLine("ReasegCedidoHogar", 1, "Pago", 1L,
                        "<Line>C</Line>")));

        assertEquals(3, files.size());
        assertTrue(files.stream().anyMatch(file -> file.getFileName()
                .equals("ReasegAlf_HogarConstitucion" + fileDate + ".xml")));
        assertTrue(files.stream().anyMatch(file -> file.getFileName()
                .equals("CoasegCed_Liberacion" + fileDate + ".xml")));
        assertTrue(files.stream().anyMatch(file -> file.getFileName()
                .equals("ReasegCed_HogarPago" + fileDate + ".xml")));
    }

    @Test
    @DisplayName("Should use the family name when there is no known prefix")
    void shouldUseFamilyNameWhenPrefixIsUnknown() {
        String fileDate = LocalDate.now()
                .format(DateTimeFormatter.ofPattern("yyyyMMdd"));

        List<ColombiaXmlFile> files = helper.buildFiles(
                Collections.singletonList(groupedLine(
                        "OtraFamilia", 1, "Pago", 1L, "<Line>A</Line>")));

        assertEquals(
                "OtraFamiliaPago" + fileDate + ".xml",
                files.get(0).getFileName());
    }

    @Test
    @DisplayName("Should keep the direct family content untouched")
    void shouldKeepDirectFamilyContentUntouched() {
        String content = "<?xml version=\"1.0\" encoding=\"UTF-8\" ?><SSC>"
                + "<Line>A</Line><Line>B</Line><Line>C</Line></SSC>";

        List<ColombiaXmlFile> files = helper.buildFiles(
                Collections.singletonList(directLine(
                        1, "SINIE", "ASSE20260827_CARSINIE_202608.XML",
                        content)));

        assertEquals(1, files.size());

        ColombiaXmlFile file = files.get(0);
        assertEquals("Directas", file.getFamily());
        assertEquals("SINIE", file.getMovementType());
        assertEquals("ASSE20260827_CARSINIE_202608.XML", file.getFileName());
        assertEquals(content, file.getContent());
        assertEquals(3, file.getLineCount());
    }

    @Test
    @DisplayName("Should count zero lines for a direct file without details")
    void shouldCountZeroLinesForEmptyDirectFile() {
        List<ColombiaXmlFile> files = helper.buildFiles(
                Collections.singletonList(directLine(
                        1, "LRVSI", "vacio.xml", "<SSC></SSC>")));

        assertEquals(0, files.get(0).getLineCount());
    }

    @Test
    @DisplayName("Should split direct files by file name")
    void shouldSplitDirectFilesByFileName() {
        List<ColombiaAccountingLine> lines = Arrays.asList(
                directLine(1, "SINIE", "sinie.xml", "<SSC><Line/></SSC>"),
                directLine(1, "LRVSI", "lrvsi.xml", "<SSC><Line/></SSC>"),
                directLine(2, "SINIE", "rvsinie.xml", "<SSC><Line/></SSC>"));

        List<ColombiaXmlFile> files = helper.buildFiles(lines);

        assertEquals(3, files.size());
    }

    @Test
    @DisplayName("Should ignore lines without content")
    void shouldIgnoreLinesWithoutContent() {
        List<ColombiaAccountingLine> lines = Arrays.asList(
                groupedLine("ReasegCardif", 1, "Pago", 1L, null),
                groupedLine("ReasegCardif", 1, "Pago", 2L, "<Line>B</Line>"));

        List<ColombiaXmlFile> files = helper.buildFiles(lines);

        assertEquals(1, files.size());
        assertEquals(1, files.get(0).getLineCount());
    }

    @Test
    @DisplayName("Should sort files by family and movement order")
    void shouldSortFilesByFamilyAndMovementOrder() {
        List<ColombiaAccountingLine> lines = Arrays.asList(
                groupedLine("ReasegCardif", 1, "RevPago", 1L, "<Line/>"),
                groupedLine("ReasegCardif", 1, "Constitucion", 1L, "<Line/>"),
                groupedLine("CoaseguroCedido", 1, "Pago", 1L, "<Line/>"));

        List<ColombiaXmlFile> files = helper.buildFiles(lines);

        assertEquals(3, files.size());
        assertEquals("CoaseguroCedido", files.get(0).getFamily());
        assertEquals("Constitucion", files.get(1).getMovementType());
        assertEquals("RevPago", files.get(2).getMovementType());
    }

    private ColombiaAccountingLine groupedLine(
            String family,
            Integer pass,
            String movementType,
            Long sequence,
            String content) {

        return ColombiaAccountingLine.builder()
                .family(family)
                .period(PERIOD)
                .pass(pass)
                .movementType(movementType)
                .sequence(sequence)
                .content(content)
                .build();
    }

    private ColombiaAccountingLine directLine(
            Integer pass,
            String journalType,
            String fileName,
            String content) {

        return ColombiaAccountingLine.builder()
                .family("Directas")
                .period(PERIOD)
                .pass(pass)
                .movementType(journalType)
                .fileName(fileName)
                .sequence(1L)
                .content(content)
                .build();
    }
}
