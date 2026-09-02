package co.com.bnpparibas.cardif.cierres.domain.util.helpers;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import org.junit.jupiter.api.Test;
import org.springframework.web.multipart.MultipartFile;

import co.com.bnpparibas.cardif.builders.ClaimAccountingBuilder;
import co.com.bnpparibas.cardif.cierres.domain.util.exception.DataException;
import co.com.bnpparibas.cardif.cierres.domain.util.helpers.ClaimFileHelper;

class ClaimFileHelperTest {

    private final ClaimFileHelper helper = new ClaimFileHelper();

    @Test
    void read_salteaLaFilaDeEncabezado() {
        String content = ClaimAccountingBuilder.csvHeader() + "\n"
                + ClaimAccountingBuilder.csvRow("022") + "\n"
                + ClaimAccountingBuilder.csvRow("023");

        List<String[]> rows = helper.read(ClaimAccountingBuilder.csvFile(content));

        assertEquals(2, rows.size());
        assertEquals("022", rows.get(0)[0]);
    }

    @Test
    void read_salteaElEncabezadoQueEmpiezaConRamo() {
        String content = ClaimAccountingBuilder.csvRow("RAMO") + "\n"
                + ClaimAccountingBuilder.csvRow("022");

        List<String[]> rows = helper.read(ClaimAccountingBuilder.csvFile(content));

        assertEquals(1, rows.size());
        assertEquals("022", rows.get(0)[0]);
    }

    @Test
    void read_sinEncabezadoConservaLaPrimeraFila() {
        String content = ClaimAccountingBuilder.csvRow("022") + "\n"
                + ClaimAccountingBuilder.csvRow("023");

        List<String[]> rows = helper.read(ClaimAccountingBuilder.csvFile(content));

        assertEquals(2, rows.size());
    }

    @Test
    void read_devuelveSiempreCuarentaYSeisColumnas() {
        String content = ClaimAccountingBuilder.csvRow("022");

        List<String[]> rows = helper.read(ClaimAccountingBuilder.csvFile(content));

        assertEquals(ClaimFileHelper.COLUMNS, rows.get(0).length);
    }

    @Test
    void read_conFilaIncompletaRellenaConNulos() {
        String content = ClaimAccountingBuilder.csvRow("022", 10);

        List<String[]> rows = helper.read(ClaimAccountingBuilder.csvFile(content));

        assertNotNull(rows.get(0)[9]);
        assertNull(rows.get(0)[10]);
        assertNull(rows.get(0)[ClaimFileHelper.COLUMNS - 1]);
    }

    @Test
    void read_conFilaMasLargaDescartaElExcedente() {
        String content = ClaimAccountingBuilder.csvRow("022", 50);

        List<String[]> rows = helper.read(ClaimAccountingBuilder.csvFile(content));

        assertEquals(ClaimFileHelper.COLUMNS, rows.get(0).length);
    }

    @Test
    void read_dejaNulosLosCamposVacios() {
        String content = "022;;VALOR";

        List<String[]> rows = helper.read(ClaimAccountingBuilder.csvFile(content));

        assertEquals("022", rows.get(0)[0]);
        assertNull(rows.get(0)[1]);
        assertEquals("VALOR", rows.get(0)[2]);
    }

    @Test
    void read_conservaLosCaracteresDeLaCodificacionDeOrigen() {
        String content = "022;BANCO DE BOGOTÁ";

        List<String[]> rows = helper.read(ClaimAccountingBuilder.csvFile(content));

        assertEquals("BANCO DE BOGOTÁ", rows.get(0)[1]);
    }

    @Test
    void read_ignoraLasLineasEnBlanco() {
        String content = ClaimAccountingBuilder.csvRow("022") + "\n\n"
                + ClaimAccountingBuilder.csvRow("023") + "\n";

        List<String[]> rows = helper.read(ClaimAccountingBuilder.csvFile(content));

        assertEquals(2, rows.size());
    }

    @Test
    void read_conSoloEncabezadoLanzaExcepcion() {
        String content = ClaimAccountingBuilder.csvHeader();

        assertThrows(DataException.class,
                () -> helper.read(ClaimAccountingBuilder.csvFile(content)));
    }

    @Test
    void read_conErrorDeLecturaLanzaExcepcion() throws IOException {
        MultipartFile file = mock(MultipartFile.class);
        when(file.getInputStream()).thenThrow(new IOException());

        assertThrows(DataException.class, () -> helper.read(file));
    }

    @Test
    void countIncomplete_cuentaLasFilasSinLaUltimaColumna() {
        String[] complete = new String[ClaimFileHelper.COLUMNS];
        Arrays.fill(complete, "V");

        String[] incomplete = new String[ClaimFileHelper.COLUMNS];

        List<String[]> rows = new ArrayList<>();
        rows.add(complete);
        rows.add(incomplete);
        rows.add(incomplete);

        assertEquals(2, helper.countIncomplete(rows));
    }

    @Test
    void countIncomplete_sinFilasIncompletasDevuelveCero() {
        String[] complete = new String[ClaimFileHelper.COLUMNS];
        Arrays.fill(complete, "V");

        assertEquals(0, helper.countIncomplete(java.util.Collections.singletonList(complete)));
    }
}
