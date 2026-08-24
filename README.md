package co.com.bnpparibas.cardif.closingclaims.domain.util.messages;

/**
 * Errores controlados del cierre de movimientos Cardif Centroamerica.
 */
public enum CardifCenterClosingMessage {

    /** La vista no devolvio movimientos para exportar a Excel. */
    NO_MOVEMENTS_TO_EXPORT("No existen movimientos para generar el archivo"),

    /** Falla al construir el archivo Excel. */
    EXCEL_GENERATION_ERROR("Error al generar el archivo Excel"),

    /** El procedimiento no devolvio lineas contables para el periodo. */
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

    CardifCenterClosingMessage(String message) {
        this.message = message;
    }

    public String getMessage() {
        return message;
    }
}
