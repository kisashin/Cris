package co.com.bnpparibas.cardif.closingclaims.domain.util.messages;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;

class ColombiaClosingMessageTest {

    @Test
    @DisplayName("Cada valor expone un mensaje no vacio")
    void everyValueHasMessage() {
        for (ColombiaClosingMessage value
                : ColombiaClosingMessage.values()) {
            assertNotNull(value.getMessage());
            assertFalse(value.getMessage().trim().isEmpty());
        }
    }

    @Test
    @DisplayName("Los mensajes corresponden a cada constante")
    void messagesMatchConstants() {
        assertEquals(
                "Debe ejecutar primero el cierre de Aval",
                ColombiaClosingMessage
                        .AVAL_CLOSING_NOT_EXECUTED.getMessage());
        assertEquals(
                "No se generaron asientos contables para el periodo",
                ColombiaClosingMessage
                        .NO_ACCOUNTING_ENTRIES_GENERATED.getMessage());
        assertEquals(
                "Error al generar los archivos XML contables",
                ColombiaClosingMessage
                        .XML_GENERATION_ERROR.getMessage());
        assertEquals(
                "El archivo XML solicitado no existe",
                ColombiaClosingMessage
                        .XML_FILE_NOT_FOUND.getMessage());
        assertEquals(
                "Error al acceder a la informacion del cierre de movimientos",
                ColombiaClosingMessage
                        .DATABASE_ACCESS_ERROR.getMessage());
        assertEquals(
                ColombiaClosingMessage.XML_FILE_NOT_FOUND,
                ColombiaClosingMessage.valueOf("XML_FILE_NOT_FOUND"));
    }
}
