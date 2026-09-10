package co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.function.Consumer;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

class AvalReportFileDTOTest {

    private AvalReportFileDTO dto() {
        return AvalReportFileDTO.builder()
                .id(1)
                .period("202609")
                .fileName("RPT_CIERRE_AVAL.xlsx")
                .rowCount(257)
                .processDate("09/09/2026 10:00:00 a. m.")
                .status("GENERADO")
                .pendingMovements(93)
                .build();
    }

    @Test
    @DisplayName("El builder asigna todos los campos")
    void builderAssignsEveryField() {
        AvalReportFileDTO result = dto();

        assertEquals(1, result.getId());
        assertEquals("202609", result.getPeriod());
        assertEquals("RPT_CIERRE_AVAL.xlsx", result.getFileName());
        assertEquals(257, result.getRowCount());
        assertEquals("09/09/2026 10:00:00 a. m.", result.getProcessDate());
        assertEquals("GENERADO", result.getStatus());
        assertEquals(93, result.getPendingMovements());
    }

    @Test
    @DisplayName("Los setters asignan todos los campos")
    void settersAssignEveryField() {
        AvalReportFileDTO result = new AvalReportFileDTO();

        assertNull(result.getId());
        assertEquals(0, result.getPendingMovements());

        result.setId(2);
        result.setPeriod("202608");
        result.setFileName("otro.xlsx");
        result.setRowCount(10);
        result.setProcessDate("fecha");
        result.setStatus("GENERADO");
        result.setPendingMovements(5);

        assertEquals(2, result.getId());
        assertEquals("202608", result.getPeriod());
        assertEquals("otro.xlsx", result.getFileName());
        assertEquals(10, result.getRowCount());
        assertEquals("fecha", result.getProcessDate());
        assertEquals("GENERADO", result.getStatus());
        assertEquals(5, result.getPendingMovements());
    }

    @Test
    @DisplayName("El constructor con todos los argumentos asigna los campos")
    void allArgsConstructor() {
        AvalReportFileDTO result = new AvalReportFileDTO(
                3, "202609", "f.xlsx", 1, "fecha", "GENERADO", 7);

        assertNotNull(result);
        assertEquals(3, result.getId());
        assertEquals(7, result.getPendingMovements());
    }

    @Test
    @DisplayName("equals, hashCode y toString reflejan el contenido")
    void equalsHashCodeAndToString() {
        AvalReportFileDTO first = dto();
        AvalReportFileDTO second = dto();

        assertEquals(first, second);
        assertEquals(first, first);
        assertEquals(first.hashCode(), second.hashCode());
        assertNotEquals(first, null);
        assertNotEquals(first, "otro tipo");
        assertNotEquals(first, new AvalReportFileDTO());
        assertTrue(first.toString().contains("RPT_CIERRE_AVAL.xlsx"));
    }

    @Test
    @DisplayName("equals detecta diferencias en cualquier campo")
    void equalsDetectsEveryFieldDifference() {
        assertNotEquals(dto(), modified(d -> d.setId(99)));
        assertNotEquals(dto(), modified(d -> d.setPeriod("X")));
        assertNotEquals(dto(), modified(d -> d.setFileName("X")));
        assertNotEquals(dto(), modified(d -> d.setRowCount(99)));
        assertNotEquals(dto(), modified(d -> d.setProcessDate("X")));
        assertNotEquals(dto(), modified(d -> d.setStatus("X")));
        assertNotEquals(dto(), modified(d -> d.setPendingMovements(0)));
    }

    @Test
    @DisplayName("equals compara correctamente los campos nulos")
    void equalsHandlesNullFields() {
        AvalReportFileDTO empty = new AvalReportFileDTO();
        AvalReportFileDTO other = new AvalReportFileDTO();

        assertEquals(empty, other);
        assertEquals(empty.hashCode(), other.hashCode());

        other.setId(1);
        assertNotEquals(empty, other);
        assertNotEquals(other, empty);
        assertNotNull(empty.toString());
    }

    private AvalReportFileDTO modified(Consumer<AvalReportFileDTO> change) {
        AvalReportFileDTO result = dto();
        change.accept(result);
        return result;
    }
}
