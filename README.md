package co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.Collections;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;

class ColombiaDtosTest {

    @Test
    @DisplayName("ColombiaAccountingLine builder asigna los valores")
    void accountingLineBuilder() {
        ColombiaAccountingLine line = ColombiaAccountingLine.builder()
                .family("ReasegCardif")
                .period("202608")
                .pass(1)
                .movementType("Pago")
                .fileName("archivo.xml")
                .sequence(3L)
                .content("<Line/>")
                .build();

        assertEquals("ReasegCardif", line.getFamily());
        assertEquals("202608", line.getPeriod());
        assertEquals(1, line.getPass());
        assertEquals("Pago", line.getMovementType());
        assertEquals("archivo.xml", line.getFileName());
        assertEquals(3L, line.getSequence());
        assertEquals("<Line/>", line.getContent());
    }

    @Test
    @DisplayName("ColombiaAccountingLine setters y constructores")
    void accountingLineSetters() {
        ColombiaAccountingLine line = new ColombiaAccountingLine();

        line.setFamily("Directas");
        line.setPeriod("202607");
        line.setPass(2);
        line.setMovementType("SINIE");
        line.setFileName("directas.xml");
        line.setSequence(1L);
        line.setContent("<SSC/>");

        assertEquals("Directas", line.getFamily());
        assertEquals("202607", line.getPeriod());
        assertEquals(2, line.getPass());
        assertEquals("SINIE", line.getMovementType());
        assertEquals("directas.xml", line.getFileName());
        assertEquals(1L, line.getSequence());
        assertEquals("<SSC/>", line.getContent());

        ColombiaAccountingLine full = new ColombiaAccountingLine(
                "CoaseguroCedido", "202608", 1, "Liberacion",
                null, 5L, "<Line/>");

        assertEquals("CoaseguroCedido", full.getFamily());
        assertNull(full.getFileName());
    }

    @Test
    @DisplayName("ColombiaXmlFile builder, setters y constructores")
    void xmlFile() {
        ColombiaXmlFile file = ColombiaXmlFile.builder()
                .family("ReasegAlfa")
                .period("202608")
                .movementType("Constitucion")
                .fileName("ReasegAlf_HogarConstitucion20260827.xml")
                .lineCount(4)
                .content("<SSC/>")
                .build();

        assertEquals("ReasegAlfa", file.getFamily());
        assertEquals("202608", file.getPeriod());
        assertEquals("Constitucion", file.getMovementType());
        assertEquals(
                "ReasegAlf_HogarConstitucion20260827.xml",
                file.getFileName());
        assertEquals(4, file.getLineCount());
        assertEquals("<SSC/>", file.getContent());

        ColombiaXmlFile empty = new ColombiaXmlFile();
        empty.setFamily("Directas");
        empty.setLineCount(2);
        assertEquals("Directas", empty.getFamily());
        assertEquals(2, empty.getLineCount());

        ColombiaXmlFile full = new ColombiaXmlFile(
                "Directas", "202608", "SINIE", "f.xml", 1, "<SSC/>");
        assertEquals("SINIE", full.getMovementType());
    }

    @Test
    @DisplayName("ColombiaXmlFileDTO builder, setters y constructores")
    void xmlFileDto() {
        ColombiaXmlFileDTO dto = ColombiaXmlFileDTO.builder()
                .id(1)
                .period("202608")
                .family("ReasegCardif")
                .movementType("Pago")
                .fileName("archivo.xml")
                .lineCount(10)
                .processDate("27/08/2026 10:00:00 a. m.")
                .status("GENERADO")
                .build();

        assertEquals(1, dto.getId());
        assertEquals("202608", dto.getPeriod());
        assertEquals("ReasegCardif", dto.getFamily());
        assertEquals("Pago", dto.getMovementType());
        assertEquals("archivo.xml", dto.getFileName());
        assertEquals(10, dto.getLineCount());
        assertEquals("27/08/2026 10:00:00 a. m.", dto.getProcessDate());
        assertEquals("GENERADO", dto.getStatus());

        ColombiaXmlFileDTO empty = new ColombiaXmlFileDTO();
        empty.setId(2);
        empty.setStatus("GENERADO");
        assertEquals(2, empty.getId());
        assertEquals("GENERADO", empty.getStatus());

        ColombiaXmlFileDTO full = new ColombiaXmlFileDTO(
                3, "202608", "Directas", "SINIE",
                "f.xml", 1, "fecha", "GENERADO");
        assertEquals(3, full.getId());
    }

    @Test
    @DisplayName("ColombiaAccountingResultDTO builder, setters y constructores")
    void resultDto() {
        List<ColombiaXmlFileDTO> files = Collections.singletonList(
                ColombiaXmlFileDTO.builder().id(1).build());

        ColombiaAccountingResultDTO result =
                ColombiaAccountingResultDTO.builder()
                        .message("Asientos generados con éxito.")
                        .period("202608")
                        .files(files)
                        .build();

        assertEquals("Asientos generados con éxito.", result.getMessage());
        assertEquals("202608", result.getPeriod());
        assertNotNull(result.getFiles());
        assertEquals(1, result.getFiles().size());

        ColombiaAccountingResultDTO empty =
                new ColombiaAccountingResultDTO();
        empty.setMessage("otro");
        empty.setPeriod("202607");
        empty.setFiles(Collections.emptyList());
        assertEquals("otro", empty.getMessage());
        assertEquals("202607", empty.getPeriod());
        assertEquals(0, empty.getFiles().size());

        ColombiaAccountingResultDTO full =
                new ColombiaAccountingResultDTO("msg", "202608", files);
        assertEquals("msg", full.getMessage());
    }
}
