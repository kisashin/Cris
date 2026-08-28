package co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ColombiaAccountingLineTest {

    private ColombiaAccountingLine line() {
        return ColombiaAccountingLine.builder()
                .family("ReasegCardif")
                .period("202608")
                .pass(1)
                .movementType("Pago")
                .fileName("archivo.xml")
                .sequence(3L)
                .content("<Line/>")
                .build();
    }

    @Test
    @DisplayName("El builder asigna todos los campos")
    void builderAssignsEveryField() {
        ColombiaAccountingLine result = line();

        assertEquals("ReasegCardif", result.getFamily());
        assertEquals("202608", result.getPeriod());
        assertEquals(1, result.getPass());
        assertEquals("Pago", result.getMovementType());
        assertEquals("archivo.xml", result.getFileName());
        assertEquals(3L, result.getSequence());
        assertEquals("<Line/>", result.getContent());
    }

    @Test
    @DisplayName("Los setters asignan todos los campos")
    void settersAssignEveryField() {
        ColombiaAccountingLine result = new ColombiaAccountingLine();

        assertNull(result.getFamily());

        result.setFamily("Directas");
        result.setPeriod("202607");
        result.setPass(2);
        result.setMovementType("SINIE");
        result.setFileName("directas.xml");
        result.setSequence(1L);
        result.setContent("<SSC/>");

        assertEquals("Directas", result.getFamily());
        assertEquals("202607", result.getPeriod());
        assertEquals(2, result.getPass());
        assertEquals("SINIE", result.getMovementType());
        assertEquals("directas.xml", result.getFileName());
        assertEquals(1L, result.getSequence());
        assertEquals("<SSC/>", result.getContent());
    }

    @Test
    @DisplayName("El constructor con todos los argumentos asigna los campos")
    void allArgsConstructor() {
        ColombiaAccountingLine result = new ColombiaAccountingLine(
                "CoaseguroCedido", "202608", 1, "Liberacion",
                null, 5L, "<Line/>");

        assertNotNull(result);
        assertEquals("CoaseguroCedido", result.getFamily());
        assertNull(result.getFileName());
        assertEquals(5L, result.getSequence());
    }

    @Test
    @DisplayName("equals, hashCode y toString reflejan el contenido")
    void equalsHashCodeAndToString() {
        ColombiaAccountingLine first = line();
        ColombiaAccountingLine second = line();
        ColombiaAccountingLine different = line();
        different.setFamily("Directas");

        assertEquals(first, second);
        assertEquals(first, first);
        assertEquals(first.hashCode(), second.hashCode());
        assertNotEquals(first, different);
        assertNotEquals(first, null);
        assertNotEquals(first, "otro tipo");
        assertNotEquals(first, new ColombiaAccountingLine());
        assertTrue(first.toString().contains("ReasegCardif"));
    }
}
