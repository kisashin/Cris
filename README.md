package co.com.bnpparibas.cardif.closingclaims.domain.util.messages;

/**
 * Errores controlados del reporte mensual de Aval.
 */
public enum AvalReportMessage {

    /** No existen movimientos pendientes para reportar. */
    NO_MOVEMENTS_TO_EXPORT(
            "No existen movimientos para generar el archivo"),

    /** Falla al construir el archivo Excel. */
    EXCEL_GENERATION_ERROR("Error al generar el archivo Excel"),

    /** Falla al acceder a la base de datos del reporte. */
    DATABASE_ACCESS_ERROR(
            "Error al acceder a la informacion del reporte de Aval");

    private final String message;

    AvalReportMessage(String message) {
        this.message = message;
    }

    public String getMessage() {
        return message;
    }
}
