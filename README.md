package co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ColombiaXmlFileTest {

    private ColombiaXmlFile file() {
        return ColombiaXmlFile.builder()
                .family("ReasegAlfa")
                .period("202608")
                .movementType("Constitucion")
                .fileName("ReasegAlf_HogarConstitucion20260827.xml")
                .lineCount(4)
                .content("<SSC/>")
                .build();
    }

    @Test
    @DisplayName("El builder asigna todos los campos")
    void builderAssignsEveryField() {
        ColombiaXmlFile result = file();

        assertEquals("ReasegAlfa", result.getFamily());
        assertEquals("202608", result.getPeriod());
        assertEquals("Constitucion", result.getMovementType());
        assertEquals(
                "ReasegAlf_HogarConstitucion20260827.xml",
                result.getFileName());
        assertEquals(4, result.getLineCount());
        assertEquals("<SSC/>", result.getContent());
    }

    @Test
    @DisplayName("Los setters asignan todos los campos")
    void settersAssignEveryField() {
        ColombiaXmlFile result = new ColombiaXmlFile();

        assertNull(result.getFamily());

        result.setFamily("Directas");
        result.setPeriod("202607");
        result.setMovementType("SINIE");
        result.setFileName("directas.xml");
        result.setLineCount(2);
        result.setContent("<SSC/>");

        assertEquals("Directas", result.getFamily());
        assertEquals("202607", result.getPeriod());
        assertEquals("SINIE", result.getMovementType());
        assertEquals("directas.xml", result.getFileName());
        assertEquals(2, result.getLineCount());
        assertEquals("<SSC/>", result.getContent());
    }

    @Test
    @DisplayName("El constructor con todos los argumentos asigna los campos")
    void allArgsConstructor() {
        ColombiaXmlFile result = new ColombiaXmlFile(
                "Directas", "202608", "SINIE", "f.xml", 1, "<SSC/>");

        assertNotNull(result);
        assertEquals("Directas", result.getFamily());
        assertEquals("SINIE", result.getMovementType());
        assertEquals(1, result.getLineCount());
    }

    @Test
    @DisplayName("equals, hashCode y toString reflejan el contenido")
    void equalsHashCodeAndToString() {
        ColombiaXmlFile first = file();
        ColombiaXmlFile second = file();
        ColombiaXmlFile different = file();
        different.setLineCount(9);

        assertEquals(first, second);
        assertEquals(first, first);
        assertEquals(first.hashCode(), second.hashCode());
        assertNotEquals(first, different);
        assertNotEquals(first, null);
        assertNotEquals(first, "otro tipo");
        assertNotEquals(first, new ColombiaXmlFile());
        assertTrue(first.toString().contains("ReasegAlfa"));
    }
}
