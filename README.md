package co.com.bnpparibas.cardif.closingclaims.domain.entity;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.time.LocalDateTime;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;

class ArchivoAsientoXmlTest {

    private static final LocalDateTime PROCESS_DATE =
            LocalDateTime.of(2026, 8, 27, 10, 15, 30);

    @Test
    @DisplayName("ArchivoAsientoCardifXml builder asigna los valores")
    void cardifBuilder() {
        ArchivoAsientoCardifXml entity = ArchivoAsientoCardifXml.builder()
                .id(1)
                .idLote("lote-1")
                .periodo("202608")
                .familia("ReasegCardif")
                .tipoMovimiento("Pago")
                .nombreArchivo("archivo.xml")
                .contenido("<SSC/>")
                .cantidadLineas(4)
                .fechaproceso(PROCESS_DATE)
                .estado("GENERADO")
                .build();

        assertEquals(1, entity.getId());
        assertEquals("lote-1", entity.getIdLote());
        assertEquals("202608", entity.getPeriodo());
        assertEquals("ReasegCardif", entity.getFamilia());
        assertEquals("Pago", entity.getTipoMovimiento());
        assertEquals("archivo.xml", entity.getNombreArchivo());
        assertEquals("<SSC/>", entity.getContenido());
        assertEquals(4, entity.getCantidadLineas());
        assertEquals(PROCESS_DATE, entity.getFechaproceso());
        assertEquals("GENERADO", entity.getEstado());
    }

    @Test
    @DisplayName("ArchivoAsientoCardifXml setters y constructores")
    void cardifSetters() {
        ArchivoAsientoCardifXml entity = new ArchivoAsientoCardifXml();

        assertNull(entity.getId());

        entity.setId(2);
        entity.setIdLote("lote-2");
        entity.setPeriodo("202607");
        entity.setFamilia("Directas");
        entity.setTipoMovimiento("SINIE");
        entity.setNombreArchivo("directas.xml");
        entity.setContenido("<SSC/>");
        entity.setCantidadLineas(9);
        entity.setFechaproceso(PROCESS_DATE);
        entity.setEstado("GENERADO");

        assertEquals(2, entity.getId());
        assertEquals("lote-2", entity.getIdLote());
        assertEquals("202607", entity.getPeriodo());
        assertEquals("Directas", entity.getFamilia());
        assertEquals("SINIE", entity.getTipoMovimiento());
        assertEquals("directas.xml", entity.getNombreArchivo());
        assertEquals("<SSC/>", entity.getContenido());
        assertEquals(9, entity.getCantidadLineas());
        assertEquals(PROCESS_DATE, entity.getFechaproceso());
        assertEquals("GENERADO", entity.getEstado());

        ArchivoAsientoCardifXml full = new ArchivoAsientoCardifXml(
                3, "lote-3", "202608", "CoaseguroCedido", "Liberacion",
                "f.xml", "<SSC/>", 1, PROCESS_DATE, "GENERADO");

        assertNotNull(full);
        assertEquals(3, full.getId());
        assertEquals("CoaseguroCedido", full.getFamilia());
    }

    @Test
    @DisplayName("ArchivoAsientoAvalXml builder asigna los valores")
    void avalBuilder() {
        ArchivoAsientoAvalXml entity = ArchivoAsientoAvalXml.builder()
                .id(1)
                .idLote("lote-1")
                .periodo("202608")
                .familia("ReasegAlfa")
                .tipoMovimiento("Constitucion")
                .nombreArchivo("archivo.xml")
                .contenido("<SSC/>")
                .cantidadLineas(6)
                .fechaproceso(PROCESS_DATE)
                .estado("GENERADO")
                .build();

        assertEquals(1, entity.getId());
        assertEquals("lote-1", entity.getIdLote());
        assertEquals("202608", entity.getPeriodo());
        assertEquals("ReasegAlfa", entity.getFamilia());
        assertEquals("Constitucion", entity.getTipoMovimiento());
        assertEquals("archivo.xml", entity.getNombreArchivo());
        assertEquals("<SSC/>", entity.getContenido());
        assertEquals(6, entity.getCantidadLineas());
        assertEquals(PROCESS_DATE, entity.getFechaproceso());
        assertEquals("GENERADO", entity.getEstado());
    }

    @Test
    @DisplayName("ArchivoAsientoAvalXml setters y constructores")
    void avalSetters() {
        ArchivoAsientoAvalXml entity = new ArchivoAsientoAvalXml();

        assertNull(entity.getId());

        entity.setId(2);
        entity.setIdLote("lote-2");
        entity.setPeriodo("202607");
        entity.setFamilia("Directas");
        entity.setTipoMovimiento("CRVSI");
        entity.setNombreArchivo("directas.xml");
        entity.setContenido("<SSC/>");
        entity.setCantidadLineas(3);
        entity.setFechaproceso(PROCESS_DATE);
        entity.setEstado("GENERADO");

        assertEquals(2, entity.getId());
        assertEquals("lote-2", entity.getIdLote());
        assertEquals("202607", entity.getPeriodo());
        assertEquals("Directas", entity.getFamilia());
        assertEquals("CRVSI", entity.getTipoMovimiento());
        assertEquals("directas.xml", entity.getNombreArchivo());
        assertEquals("<SSC/>", entity.getContenido());
        assertEquals(3, entity.getCantidadLineas());
        assertEquals(PROCESS_DATE, entity.getFechaproceso());
        assertEquals("GENERADO", entity.getEstado());

        ArchivoAsientoAvalXml full = new ArchivoAsientoAvalXml(
                3, "lote-3", "202608", "ReasegAlfa", "Pago",
                "f.xml", "<SSC/>", 1, PROCESS_DATE, "GENERADO");

        assertNotNull(full);
        assertEquals(3, full.getId());
        assertEquals("ReasegAlfa", full.getFamilia());
    }
}
