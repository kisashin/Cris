package co.com.bnpparibas.cardif.closingclaims.domain.util.messages;

/**
 * Catálogo centralizado de los errores controlados del cierre de movimientos
 * Cardif Centroamérica.
 *
 * <p>Reúne en un único lugar los errores que el módulo sabe de antemano que
 * pueden ocurrir y maneja de forma controlada (se capturan y se devuelven como
 * {@link co.com.bnpparibas.cardif.closingclaims.domain.util.exception.BusinessException}
 * con su {@code HttpStatus}). Permite conocer los posibles fallos sin revisar
 * las clases de servicio.</p>
 *
 * <p>No incluye mensajes de flujo normal (éxito o informativos), que viven en
 * el servicio, ni los textos de log (contexto técnico con {@code correlationId}
 * y {@code requestId}).</p>
 */
public enum CardifCenterClosingMessage {

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
