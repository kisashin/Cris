package co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

class AvalReportStatusDTOTest {

    private AvalReportStatusDTO status() {
        return AvalReportStatusDTO.builder()
                .generationDate("27/08/2026 10:00:00 a. m.")
                .pendingMovements(93)
                .build();
    }

    @Test
    @DisplayName("El builder asigna todos los campos")
    void builderAssignsEveryField() {
        AvalReportStatusDTO dto = status();

        assertEquals("27/08/2026 10:00:00 a. m.", dto.getGenerationDate());
        assertEquals(93, dto.getPendingMovements());
    }

    @Test
    @DisplayName("Los setters asignan todos los campos")
    void settersAssignEveryField() {
        AvalReportStatusDTO dto = new AvalReportStatusDTO();

        assertNull(dto.getGenerationDate());
        assertEquals(0, dto.getPendingMovements());

        dto.setGenerationDate("fecha");
        dto.setPendingMovements(7);

        assertEquals("fecha", dto.getGenerationDate());
        assertEquals(7, dto.getPendingMovements());
    }

    @Test
    @DisplayName("El constructor con todos los argumentos asigna los campos")
    void allArgsConstructor() {
        AvalReportStatusDTO dto =
                new AvalReportStatusDTO("otra fecha", 5);

        assertNotNull(dto);
        assertEquals("otra fecha", dto.getGenerationDate());
        assertEquals(5, dto.getPendingMovements());
    }

    @Test
    @DisplayName("equals, hashCode y toString reflejan el contenido")
    void equalsHashCodeAndToString() {
        AvalReportStatusDTO first = status();
        AvalReportStatusDTO second = status();
        AvalReportStatusDTO different = status();
        different.setPendingMovements(1);

        assertEquals(first, second);
        assertEquals(first, first);
        assertEquals(first.hashCode(), second.hashCode());
        assertNotEquals(first, different);
        assertNotEquals(first, null);
        assertNotEquals(first, "otro tipo");
        assertNotEquals(first, new AvalReportStatusDTO());
        assertTrue(first.toString().contains("93"));
    }
}
