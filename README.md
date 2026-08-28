package co.com.bnpparibas.cardif.closingclaims.domain.util.helpers;

import co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia.AvalReportRow;
import org.apache.poi.util.DefaultTempFileCreationStrategy;
import org.apache.poi.util.TempFile;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.io.File;
import java.io.IOException;
import java.math.BigDecimal;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

class AvalReportExcelHelperTest {

    private static final File POI_TEMP_DIR =
            new File("target/poi-files-aval");

    private final AvalReportExcelHelper helper =
            new AvalReportExcelHelper();

    @BeforeAll
    static void redirectPoiTempFiles() {
        POI_TEMP_DIR.mkdirs();
        TempFile.setTempFileCreationStrategy(
                new DefaultTempFileCreationStrategy(POI_TEMP_DIR));
    }

    @AfterAll
    static void resetPoiTempFiles() {
        TempFile.setTempFileCreationStrategy(
                new DefaultTempFileCreationStrategy());
    }

    @Test
    @DisplayName("Should generate a valid Excel with header and data rows")
    void shouldGenerateValidExcelWithData() throws IOException {
        AvalReportRow row = AvalReportRow.builder()
                .compania("02")
                .sucursal("02")
                .descripcionRamo("VIDA GRUPO")
                .symbol("VG")
                .ramo2(34)
                .nroPoliza("1234567890")
                .modulo("00")
                .codBancoNegocio("4020")
                .descripcionTomador("Banco de Bogota")
                .siniestroLider("0902026A193877HC")
                .valor(0)
                .numeroLote(0)
                .campoUnion("0902026A193877HC")
                .valorInicialReserva(new BigDecimal("1500000.00"))
                .valorAjustesReserva(BigDecimal.ZERO)
                .valorPagos(BigDecimal.ZERO)
                .valorActualReserva(BigDecimal.ZERO)
                .porcentajeAlfa(100)
                .valorGastosCoaseguro(0)
                .valorSalvamento(0)
                .valorRecuperaciones(0)
                .nroidentificacion("1020304050")
                .nombreasegurado("JUAN PEREZ")
                .fechanacimiento("19800101")
                .edad(45)
                .sexo("M")
                .profesion("INGENIERO")
                .codigoCausa("HC")
                .causaSiniestro("MUERTE ACCIDENTAL")
                .ciudad("BOGOTA")
                .tipoSiniestro("OT")
                .nroCredito("00998877")
                .porcentajeAsegurabilidad("100")
                .tipocredito("LIBRE INVERSION")
                .coberturaLider("MUERTE ACCIDENTAL")
                .reportadoPor("Reserva Inicial - Re-Aseguradora")
                .nitBeneficiario("8600029644")
                .beneficiario("Banco de Bogota")
                .build();

        AvalReportRow secondRow = AvalReportRow.builder()
                .compania("02")
                .siniestroLider("0902026A193878HC")
                .valorPagos(new BigDecimal("250000.00"))
                .edad(30)
                .build();

        List<AvalReportRow> rows = Arrays.asList(row, secondRow);

        byte[] result = helper.generateExcel(rows);

        assertNotNull(result);
        assertTrue(result.length > 0);
        assertValidOoxml(result);
    }

    @Test
    @DisplayName("Should generate a valid Excel with only headers when list is empty")
    void shouldGenerateValidExcelWhenListIsEmpty() throws IOException {
        byte[] result = helper.generateExcel(Collections.emptyList());

        assertNotNull(result);
        assertTrue(result.length > 0);
        assertValidOoxml(result);
    }

    @Test
    @DisplayName("Should generate a valid Excel when every value is null")
    void shouldGenerateValidExcelWithNullValues() throws IOException {
        byte[] result = helper.generateExcel(
                Collections.singletonList(new AvalReportRow()));

        assertNotNull(result);
        assertTrue(result.length > 0);
        assertValidOoxml(result);
    }

    private void assertValidOoxml(byte[] content) {
        assertTrue(content.length >= 2, "El archivo no debe estar vacío");
        assertTrue(
                content[0] == 0x50 && content[1] == 0x4B,
                "El archivo debe iniciar con la firma OOXML/ZIP (PK)");
    }
}
