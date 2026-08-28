package co.com.bnpparibas.cardif.closingclaims.domain.dtos.cardifcenterclosing;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.Collections;
import java.util.List;
import java.util.function.Consumer;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

class CenterAccountingResultDTOTest {

    private List<AccountingXmlFileDTO> files() {
        return Collections.singletonList(
                AccountingXmlFileDTO.builder().id(1).build());
    }

    private CenterAccountingResultDTO result() {
        return CenterAccountingResultDTO.builder()
                .message("Asientos generados con éxito.")
                .period("202608")
                .files(files())
                .build();
    }

    @Test
    @DisplayName("El builder asigna todos los campos")
    void builderAssignsEveryField() {
        CenterAccountingResultDTO dto = result();

        assertEquals("Asientos generados con éxito.", dto.getMessage());
        assertEquals("202608", dto.getPeriod());
        assertNotNull(dto.getFiles());
        assertEquals(1, dto.getFiles().size());
    }

    @Test
    @DisplayName("Los setters asignan todos los campos")
    void settersAssignEveryField() {
        CenterAccountingResultDTO dto = new CenterAccountingResultDTO();

        assertNull(dto.getMessage());

        dto.setMessage("otro");
        dto.setPeriod("202607");
        dto.setFiles(Collections.emptyList());

        assertEquals("otro", dto.getMessage());
        assertEquals("202607", dto.getPeriod());
        assertEquals(0, dto.getFiles().size());
    }

    @Test
    @DisplayName("El constructor con todos los argumentos asigna los campos")
    void allArgsConstructor() {
        CenterAccountingResultDTO dto = new CenterAccountingResultDTO(
                "msg", "202608", files());

        assertNotNull(dto);
        assertEquals("msg", dto.getMessage());
        assertEquals(1, dto.getFiles().size());
    }

    @Test
    @DisplayName("equals, hashCode y toString reflejan el contenido")
    void equalsHashCodeAndToString() {
        CenterAccountingResultDTO first = result();
        CenterAccountingResultDTO second = result();

        assertEquals(first, second);
        assertEquals(first, first);
        assertEquals(first.hashCode(), second.hashCode());
        assertNotEquals(first, null);
        assertNotEquals(first, "otro tipo");
        assertNotEquals(first, new CenterAccountingResultDTO());
        assertTrue(first.toString().contains("202608"));
    }

    @Test
    @DisplayName("equals detecta diferencias en cualquier campo")
    void equalsDetectsEveryFieldDifference() {
        assertNotEquals(result(), modified(d -> d.setMessage("X")));
        assertNotEquals(result(), modified(d -> d.setPeriod("X")));
        assertNotEquals(result(),
                modified(d -> d.setFiles(Collections.emptyList())));
    }

    @Test
    @DisplayName("equals compara correctamente los campos nulos")
    void equalsHandlesNullFields() {
        CenterAccountingResultDTO empty = new CenterAccountingResultDTO();
        CenterAccountingResultDTO other = new CenterAccountingResultDTO();

        assertEquals(empty, other);
        assertEquals(empty.hashCode(), other.hashCode());

        other.setMessage("msg");
        assertNotEquals(empty, other);
        assertNotEquals(other, empty);
        assertNotNull(empty.toString());
    }

    private CenterAccountingResultDTO modified(
            Consumer<CenterAccountingResultDTO> change) {
        CenterAccountingResultDTO result = result();
        change.accept(result);
        return result;
    }
}
