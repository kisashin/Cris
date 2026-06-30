CardifCenterClosingMessage

package co.com.bnpparibas.cardif.closingclaims.domain.util.messages;

/**
 * Catálogo centralizado de los mensajes de salida del cierre de movimientos
 * Cardif Centroamérica.
 *
 * <p>Reúne en un único lugar los textos que el módulo devuelve al usuario,
 * tanto los de respuesta exitosa como los de las excepciones de negocio, para
 * poder consultarlos sin revisar las clases de servicio.</p>
 *
 * <p>No incluye los textos de log (contexto técnico con {@code correlationId}
 * y {@code requestId}); esos permanecen junto a la traza en el servicio.</p>
 */
public enum CardifCenterClosingMessage {

    /** Contabilización ejecutada correctamente. */
    ACCOUNTING_ENTRIES_GENERATED("Asientos generados con éxito."),

    /** No había movimientos pendientes por contabilizar. */
    NO_PENDING_MOVEMENTS("No hay movimientos para contabilizar."),

    /** La vista no devolvió movimientos para exportar a Excel. */
    NO_MOVEMENTS_TO_EXPORT("No existen movimientos para generar el archivo"),

    /** Falla al construir el archivo Excel. */
    EXCEL_GENERATION_ERROR("Error al generar el archivo Excel"),

    /** Falla al acceder a la base de datos del cierre. */
    DATABASE_ACCESS_ERROR(
            "Error al acceder a la información del cierre de movimientos");

    private final String message;

    CardifCenterClosingMessage(String message) {
        this.message = message;
    }

    public String getMessage() {
        return message;
    }
}
