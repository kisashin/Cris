package co.com.bnpparibas.cardif.closingclaims.domain.dtos.cardifcenterclosing;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.function.Consumer;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

class AccountingXmlFileDTOTest {

    private AccountingXmlFileDTO dto() {
        return AccountingXmlFileDTO.builder()
                .id(1)
                .period("202608")
                .movementType("Pago")
                .fileName("archivo.xml")
                .lineCount(10)
                .processDate("24/08/2026 03:45:30 p. m.")
                .status("GENERADO")
                .build();
    }

    @Test
    @DisplayName("El builder asigna todos los campos")
    void builderAssignsEveryField() {
        AccountingXmlFileDTO result = dto();

        assertEquals(1, result.getId());
        assertEquals("202608", result.getPeriod());
        assertEquals("Pago", result.getMovementType());
        assertEquals("archivo.xml", result.getFileName());
        assertEquals(10, result.getLineCount());
        assertEquals("24/08/2026 03:45:30 p. m.", result.getProcessDate());
        assertEquals("GENERADO", result.getStatus());
    }

    @Test
    @DisplayName("Los setters asignan todos los campos")
    void settersAssignEveryField() {
        AccountingXmlFileDTO result = new AccountingXmlFileDTO();

        assertNull(result.getId());

        result.setId(2);
        result.setPeriod("202607");
        result.setMovementType("Constitucion");
        result.setFileName("otro.xml");
        result.setLineCount(3);
        result.setProcessDate("fecha");
        result.setStatus("GENERADO");

        assertEquals(2, result.getId());
        assertEquals("202607", result.getPeriod());
        assertEquals("Constitucion", result.getMovementType());
        assertEquals("otro.xml", result.getFileName());
        assertEquals(3, result.getLineCount());
        assertEquals("fecha", result.getProcessDate());
        assertEquals("GENERADO", result.getStatus());
    }

    @Test
    @DisplayName("El constructor con todos los argumentos asigna los campos")
    void allArgsConstructor() {
        AccountingXmlFileDTO result = new AccountingXmlFileDTO(
                3, "202608", "Liberacion", "f.xml", 1,
                "fecha", "GENERADO");

        assertNotNull(result);
        assertEquals(3, result.getId());
        assertEquals("GENERADO", result.getStatus());
    }

    @Test
    @DisplayName("equals, hashCode y toString reflejan el contenido")
    void equalsHashCodeAndToString() {
        AccountingXmlFileDTO first = dto();
        AccountingXmlFileDTO second = dto();

        assertEquals(first, second);
        assertEquals(first, first);
        assertEquals(first.hashCode(), second.hashCode());
        assertNotEquals(first, null);
        assertNotEquals(first, "otro tipo");
        assertNotEquals(first, new AccountingXmlFileDTO());
        assertTrue(first.toString().contains("archivo.xml"));
    }

    @Test
    @DisplayName("equals detecta diferencias en cualquier campo")
    void equalsDetectsEveryFieldDifference() {
        assertNotEquals(dto(), modified(d -> d.setId(99)));
        assertNotEquals(dto(), modified(d -> d.setPeriod("X")));
        assertNotEquals(dto(), modified(d -> d.setMovementType("X")));
        assertNotEquals(dto(), modified(d -> d.setFileName("X")));
        assertNotEquals(dto(), modified(d -> d.setLineCount(99)));
        assertNotEquals(dto(), modified(d -> d.setProcessDate("X")));
        assertNotEquals(dto(), modified(d -> d.setStatus("X")));
    }

    @Test
    @DisplayName("equals compara correctamente los campos nulos")
    void equalsHandlesNullFields() {
        AccountingXmlFileDTO empty = new AccountingXmlFileDTO();
        AccountingXmlFileDTO other = new AccountingXmlFileDTO();

        assertEquals(empty, other);
        assertEquals(empty.hashCode(), other.hashCode());

        other.setId(1);
        assertNotEquals(empty, other);
        assertNotEquals(other, empty);
        assertNotNull(empty.toString());
    }

    private AccountingXmlFileDTO modified(
            Consumer<AccountingXmlFileDTO> change) {
        AccountingXmlFileDTO result = dto();
        change.accept(result);
        return result;
    }
}
