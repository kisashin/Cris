package co.com.bnpparibas.cardif.closingclaims.domain.util.messages;

/**
 * Errores controlados del cierre contable de Colombia.
 */
public enum ColombiaClosingMessage {

    /** El cierre de Aval no ha sido ejecutado en el periodo. */
    AVAL_CLOSING_NOT_EXECUTED(
            "Debe ejecutar primero el cierre de Aval"),

    /** Los procedimientos no devolvieron lineas contables. */
    NO_ACCOUNTING_ENTRIES_GENERATED(
            "No se generaron asientos contables para el periodo"),

    /** Falla al construir los archivos XML contables. */
    XML_GENERATION_ERROR("Error al generar los archivos XML contables"),

    /** El archivo solicitado no existe o no tiene contenido. */
    XML_FILE_NOT_FOUND("El archivo XML solicitado no existe"),

    /** Falla al acceder a la base de datos del cierre. */
    DATABASE_ACCESS_ERROR(
            "Error al acceder a la informacion del cierre de movimientos");

    private final String message;

    ColombiaClosingMessage(String message) {
        this.message = message;
    }

    public String getMessage() {
        return message;
    }
}
