package co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ColombiaXmlFileDTOTest {

    private ColombiaXmlFileDTO dto() {
        return ColombiaXmlFileDTO.builder()
                .id(1)
                .period("202608")
                .family("ReasegCardif")
                .movementType("Pago")
                .fileName("archivo.xml")
                .lineCount(10)
                .processDate("27/08/2026 10:00:00 a. m.")
                .status("GENERADO")
                .build();
    }

    @Test
    @DisplayName("El builder asigna todos los campos")
    void builderAssignsEveryField() {
        ColombiaXmlFileDTO result = dto();

        assertEquals(1, result.getId());
        assertEquals("202608", result.getPeriod());
        assertEquals("ReasegCardif", result.getFamily());
        assertEquals("Pago", result.getMovementType());
        assertEquals("archivo.xml", result.getFileName());
        assertEquals(10, result.getLineCount());
        assertEquals("27/08/2026 10:00:00 a. m.", result.getProcessDate());
        assertEquals("GENERADO", result.getStatus());
    }

    @Test
    @DisplayName("Los setters asignan todos los campos")
    void settersAssignEveryField() {
        ColombiaXmlFileDTO result = new ColombiaXmlFileDTO();

        assertNull(result.getId());

        result.setId(2);
        result.setPeriod("202607");
        result.setFamily("Directas");
        result.setMovementType("SINIE");
        result.setFileName("directas.xml");
        result.setLineCount(3);
        result.setProcessDate("fecha");
        result.setStatus("GENERADO");

        assertEquals(2, result.getId());
        assertEquals("202607", result.getPeriod());
        assertEquals("Directas", result.getFamily());
        assertEquals("SINIE", result.getMovementType());
        assertEquals("directas.xml", result.getFileName());
        assertEquals(3, result.getLineCount());
        assertEquals("fecha", result.getProcessDate());
        assertEquals("GENERADO", result.getStatus());
    }

    @Test
    @DisplayName("El constructor con todos los argumentos asigna los campos")
    void allArgsConstructor() {
        ColombiaXmlFileDTO result = new ColombiaXmlFileDTO(
                3, "202608", "Directas", "SINIE",
                "f.xml", 1, "fecha", "GENERADO");

        assertNotNull(result);
        assertEquals(3, result.getId());
        assertEquals("GENERADO", result.getStatus());
    }

    @Test
    @DisplayName("equals, hashCode y toString reflejan el contenido")
    void equalsHashCodeAndToString() {
        ColombiaXmlFileDTO first = dto();
        ColombiaXmlFileDTO second = dto();
        ColombiaXmlFileDTO different = dto();
        different.setId(99);

        assertEquals(first, second);
        assertEquals(first, first);
        assertEquals(first.hashCode(), second.hashCode());
        assertNotEquals(first, different);
        assertNotEquals(first, null);
        assertNotEquals(first, "otro tipo");
        assertNotEquals(first, new ColombiaXmlFileDTO());
        assertTrue(first.toString().contains("ReasegCardif"));
    }
}
