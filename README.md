package co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.Collections;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ColombiaAccountingResultDTOTest {

    private List<ColombiaXmlFileDTO> files() {
        return Collections.singletonList(
                ColombiaXmlFileDTO.builder().id(1).build());
    }

    private ColombiaAccountingResultDTO result() {
        return ColombiaAccountingResultDTO.builder()
                .message("Asientos generados con éxito.")
                .period("202608")
                .files(files())
                .build();
    }

    @Test
    @DisplayName("El builder asigna todos los campos")
    void builderAssignsEveryField() {
        ColombiaAccountingResultDTO dto = result();

        assertEquals("Asientos generados con éxito.", dto.getMessage());
        assertEquals("202608", dto.getPeriod());
        assertNotNull(dto.getFiles());
        assertEquals(1, dto.getFiles().size());
    }

    @Test
    @DisplayName("Los setters asignan todos los campos")
    void settersAssignEveryField() {
        ColombiaAccountingResultDTO dto =
                new ColombiaAccountingResultDTO();

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
        ColombiaAccountingResultDTO dto =
                new ColombiaAccountingResultDTO("msg", "202608", files());

        assertNotNull(dto);
        assertEquals("msg", dto.getMessage());
        assertEquals("202608", dto.getPeriod());
        assertEquals(1, dto.getFiles().size());
    }

    @Test
    @DisplayName("equals, hashCode y toString reflejan el contenido")
    void equalsHashCodeAndToString() {
        ColombiaAccountingResultDTO first = result();
        ColombiaAccountingResultDTO second = result();
        ColombiaAccountingResultDTO different = result();
        different.setPeriod("202607");

        assertEquals(first, second);
        assertEquals(first, first);
        assertEquals(first.hashCode(), second.hashCode());
        assertNotEquals(first, different);
        assertNotEquals(first, null);
        assertNotEquals(first, "otro tipo");
        assertNotEquals(first, new ColombiaAccountingResultDTO());
        assertTrue(first.toString().contains("202608"));
    }
}
