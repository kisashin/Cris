package co.com.bnpparibas.cardif.closingclaims.domain.entity;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.time.LocalDateTime;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;

class ArchivoReporteAvalExcelTest {

    private static final LocalDateTime PROCESS_DATE =
            LocalDateTime.of(2026, 9, 9, 10, 0, 0);

    private static final byte[] CONTENT = new byte[] {0x50, 0x4B, 0x03, 0x04};

    @Test
    @DisplayName("El builder asigna todos los campos")
    void builderAssignsEveryField() {
        ArchivoReporteAvalExcel entity = ArchivoReporteAvalExcel.builder()
                .id(1)
                .idLote("lote-1")
                .periodo("202609")
                .nombreArchivo("RPT_CIERRE_AVAL.xlsx")
                .contenido(CONTENT)
                .cantidadFilas(257)
                .fechaproceso(PROCESS_DATE)
                .estado("GENERADO")
                .build();

        assertEquals(1, entity.getId());
        assertEquals("lote-1", entity.getIdLote());
        assertEquals("202609", entity.getPeriodo());
        assertEquals("RPT_CIERRE_AVAL.xlsx", entity.getNombreArchivo());
        assertArrayEquals(CONTENT, entity.getContenido());
        assertEquals(257, entity.getCantidadFilas());
        assertEquals(PROCESS_DATE, entity.getFechaproceso());
        assertEquals("GENERADO", entity.getEstado());
    }

    @Test
    @DisplayName("Los setters asignan todos los campos")
    void settersAssignEveryField() {
        ArchivoReporteAvalExcel entity = new ArchivoReporteAvalExcel();

        assertNull(entity.getId());

        entity.setId(2);
        entity.setIdLote("lote-2");
        entity.setPeriodo("202608");
        entity.setNombreArchivo("otro.xlsx");
        entity.setContenido(CONTENT);
        entity.setCantidadFilas(10);
        entity.setFechaproceso(PROCESS_DATE);
        entity.setEstado("GENERADO");

        assertEquals(2, entity.getId());
        assertEquals("lote-2", entity.getIdLote());
        assertEquals("202608", entity.getPeriodo());
        assertEquals("otro.xlsx", entity.getNombreArchivo());
        assertArrayEquals(CONTENT, entity.getContenido());
        assertEquals(10, entity.getCantidadFilas());
        assertEquals(PROCESS_DATE, entity.getFechaproceso());
        assertEquals("GENERADO", entity.getEstado());
    }

    @Test
    @DisplayName("El constructor con todos los argumentos asigna los campos")
    void allArgsConstructor() {
        ArchivoReporteAvalExcel entity = new ArchivoReporteAvalExcel(
                3, "lote-3", "202609", "f.xlsx", CONTENT, 1,
                PROCESS_DATE, "GENERADO");

        assertNotNull(entity);
        assertEquals(3, entity.getId());
        assertEquals("GENERADO", entity.getEstado());
    }
}
