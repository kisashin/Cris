package co.com.bnpparibas.cardif.closingclaims.domain.util.messages;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;

class AvalReportMessageTest {

    @Test
    @DisplayName("Cada valor expone un mensaje no vacio")
    void everyValueHasMessage() {
        for (AvalReportMessage value : AvalReportMessage.values()) {
            assertNotNull(value.getMessage());
            assertFalse(value.getMessage().trim().isEmpty());
        }
    }

    @Test
    @DisplayName("Los mensajes corresponden a cada constante")
    void messagesMatchConstants() {
        assertEquals(
                "No existen movimientos para generar el archivo",
                AvalReportMessage.NO_MOVEMENTS_TO_EXPORT.getMessage());
        assertEquals(
                "Error al generar el archivo Excel",
                AvalReportMessage.EXCEL_GENERATION_ERROR.getMessage());
        assertEquals(
                "Error al acceder a la informacion del reporte de Aval",
                AvalReportMessage.DATABASE_ACCESS_ERROR.getMessage());
        assertEquals(
                AvalReportMessage.EXCEL_GENERATION_ERROR,
                AvalReportMessage.valueOf("EXCEL_GENERATION_ERROR"));
    }
}
