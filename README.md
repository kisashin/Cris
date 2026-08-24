package co.com.bnpparibas.cardif.closingclaims.domain.util.helpers;

import co.com.bnpparibas.cardif.closingclaims.domain.dtos.cardifcenterclosing.AccountingXmlFileDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.cardifcenterclosing.AccountingXmlLine;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Base64;
import java.util.Collections;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class CardifCenterAccountingXmlHelperTest {

    private static final String HEADER =
            "<?xml version=\"1.0\" encoding=\"UTF-8\" ?><SSC><Payload><Ledger>";
    private static final String FOOTER = "</Ledger></Payload></SSC>";

    private final CardifCenterAccountingXmlHelper helper =
            new CardifCenterAccountingXmlHelper();

    @Test
    @DisplayName("Should return empty list when there are no lines")
    void shouldReturnEmptyListWhenThereAreNoLines() {
        assertTrue(helper.buildFiles(null).isEmpty());
        assertTrue(helper.buildFiles(Collections.emptyList()).isEmpty());
    }

    @Test
    @DisplayName("Should build one file per movement type")
    void shouldBuildOneFilePerMovementType() {
        List<AccountingXmlLine> lines = new ArrayList<>(Arrays.asList(
                envelope(0, "enc", HEADER),
                detail("Pago", 1L, "<Line>PAGO-1</Line>"),
                detail("Pago", 2L, "<Line>PAGO-2</Line>"),
                detail("Constitucion", 3L, "<Line>CON-1</Line>"),
                envelope(3, "pie", FOOTER)));

        List<AccountingXmlFileDTO> files = helper.buildFiles(lines);

        assertEquals(2, files.size());
        assertEquals("Constitucion", files.get(0).getMovementType());
        assertEquals("Pago", files.get(1).getMovementType());
        assertEquals(1, files.get(0).getLineCount());
        assertEquals(2, files.get(1).getLineCount());
    }

    @Test
    @DisplayName("Should wrap details with header and footer in Base64 content")
    void shouldWrapDetailsWithHeaderAndFooter() {
        List<AccountingXmlLine> lines = new ArrayList<>(Arrays.asList(
                envelope(0, "enc", HEADER),
                detail("Liberacion", 1L, "<Line>LIB-1</Line>"),
                envelope(3, "pie", FOOTER)));

        String content = decode(helper.buildFiles(lines).get(0).getContent());

        assertEquals(HEADER + "<Line>LIB-1</Line>" + FOOTER, content);
    }

    @Test
    @DisplayName("Should name files using the legacy convention")
    void shouldNameFilesUsingLegacyConvention() {
        List<AccountingXmlLine> lines = new ArrayList<>(Arrays.asList(
                envelope(0, "enc", HEADER),
                detail("RevPago", 1L, "<Line>REV-1</Line>"),
                envelope(3, "pie", FOOTER)));

        String fileName = helper.buildFiles(lines).get(0).getFileName();

        assertTrue(fileName.startsWith("Sinie_ReasegCentro_RevPago"));
        assertTrue(fileName.endsWith(".xml"));
        assertEquals(
                "Sinie_ReasegCentro_RevPago".length() + 12,
                fileName.length());
    }

    @Test
    @DisplayName("Should ignore detail lines without content or movement type")
    void shouldIgnoreIncompleteDetailLines() {
        List<AccountingXmlLine> lines = new ArrayList<>(Arrays.asList(
                envelope(0, "enc", HEADER),
                detail(null, 1L, "<Line>NO-MV</Line>"),
                detail("Pago", 2L, null),
                detail("Pago", 3L, "<Line>PAGO-1</Line>"),
                envelope(3, "pie", FOOTER)));

        List<AccountingXmlFileDTO> files = helper.buildFiles(lines);

        assertEquals(1, files.size());
        assertEquals(1, files.get(0).getLineCount());
    }

    @Test
    @DisplayName("Should build files with empty envelopes when they are missing")
    void shouldBuildFilesWhenEnvelopesAreMissing() {
        List<AccountingXmlLine> lines = Collections.singletonList(
                detail("Objecion", 1L, "<Line>OBJ-1</Line>"));

        String content = decode(helper.buildFiles(lines).get(0).getContent());

        assertEquals("<Line>OBJ-1</Line>", content);
    }

    @Test
    @DisplayName("Should place unknown movement types at the end")
    void shouldPlaceUnknownMovementTypesAtTheEnd() {
        List<AccountingXmlLine> lines = new ArrayList<>(Arrays.asList(
                detail("Otro", 1L, "<Line>OTRO-1</Line>"),
                detail("Constitucion", 2L, "<Line>CON-1</Line>")));

        List<AccountingXmlFileDTO> files = helper.buildFiles(lines);

        assertEquals("Constitucion", files.get(0).getMovementType());
        assertEquals("Otro", files.get(1).getMovementType());
    }

    private AccountingXmlLine detail(
            String movementType,
            Long sequence,
            String content) {

        return AccountingXmlLine.builder()
                .period("202608")
                .pass(1)
                .lineType(2)
                .movementType(movementType)
                .sequence(sequence)
                .content(content)
                .build();
    }

    private AccountingXmlLine envelope(
            int lineType,
            String movementType,
            String content) {

        return AccountingXmlLine.builder()
                .period("202608")
                .pass(1)
                .lineType(lineType)
                .movementType(movementType)
                .sequence(0L)
                .content(content)
                .build();
    }

    private String decode(String base64) {
        return new String(
                Base64.getDecoder().decode(base64),
                StandardCharsets.UTF_8);
    }
}
