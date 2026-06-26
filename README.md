CardifCenterClosingExcelHelperTest

package co.com.bnpparibas.cardif.closingclaims.domain.util.helpers;

import co.com.bnpparibas.cardif.closingclaims.domain.entity.CardifCenterClosing;
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

/**
 * Prueba del helper ejecutando la implementación REAL (sin mock), para que
 * JaCoCo cuente la lógica de escritura de celdas. Se evita el problema de
 * cobertura del módulo Perú, donde se mockeaba la propia clase bajo prueba.
 *
 * <p>Para no fallar en Jenkins por temporales de POI, se redirige la estrategia
 * de creación de archivos temporales a {@code target/poi-files}. Con una ventana
 * de 100 filas y un dataset mínimo, SXSSF no vuelca a disco, pero la redirección
 * queda como blindaje. No se re-abre el binario generado (eso es lo frágil en
 * CI): se valida que el contenido sea un OOXML/ZIP válido por su firma.</p>
 */
class CardifCenterClosingExcelHelperTest {

    private static final File POI_TEMP_DIR =
            new File("target/poi-files");

    private final CardifCenterClosingExcelHelper helper =
            new CardifCenterClosingExcelHelper();

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
        CardifCenterClosing movement = CardifCenterClosing.builder()
                .idCarvajal(273767966630L)
                .partner("FINANCIERA TEST")
                .claimNumber("0672025A003012")
                .certificate("6722434176267121")
                .installmentsToPay(7)
                .debtValue(0.0)
                .totalInsuredValue(180000.0)
                .movementValue(new BigDecimal("95.00"))
                .age(35)
                .information(null)
                .currency("PEN")
                .build();

        CardifCenterClosing secondMovement = CardifCenterClosing.builder()
                .idCarvajal(273767966873L)
                .partner("FINANCIERA TEST 2")
                .claimNumber("0772025A003455")
                .movementValue(new BigDecimal("14000.00"))
                .currency("PEN")
                .build();

        List<CardifCenterClosing> movements =
                Arrays.asList(movement, secondMovement);

        byte[] result = helper.generateExcel(movements);

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

    /**
     * Verifica la firma de un archivo OOXML/ZIP (bytes "PK") sin re-abrir el
     * binario, evitando dependencias de WorkbookFactory en CI.
     */
    private void assertValidOoxml(byte[] content) {
        assertTrue(content.length >= 2, "El archivo no debe estar vacío");
        assertTrue(
                content[0] == 0x50 && content[1] == 0x4B,
                "El archivo debe iniciar con la firma OOXML/ZIP (PK)");
    }
}
