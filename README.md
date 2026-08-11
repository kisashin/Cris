package co.com.bnpparibas.cardif.closingclaims.domain.util.anums;

/**
 * Tipos de novedad que se pueden solicitar sobre un movimiento.
 */
public enum NewsType {

    /** Solicitud de actualización de los campos del movimiento. */
    ACTUALIZA,

    /** Solicitud de eliminación del movimiento. */
    ELIMINA
}


package co.com.bnpparibas.cardif.closingclaims.domain.util.messages;

/**
 * Catálogo centralizado de los errores controlados del módulo de novedades
 * individuales de movimientos.
 *
 * <p>Reúne en un único lugar los errores que el módulo sabe de antemano que
 * pueden ocurrir y maneja de forma controlada (se capturan y se devuelven como
 * {@link co.com.bnpparibas.cardif.closingclaims.domain.util.exception.BusinessException}
 * con su {@code HttpStatus}).</p>
 *
 * <p>No incluye mensajes de flujo normal (éxito o informativos), que viven en
 * el servicio, ni los textos de log.</p>
 */
public enum IndividualNewsMessage {

    /** El movimiento referenciado no existe en el histórico. */
    MOVEMENT_NOT_FOUND("No se encontró el movimiento solicitado"),

    /** La novedad no existe o ya no está pendiente de autorización. */
    NEWS_NOT_PENDING("La novedad no existe o ya fue procesada o cancelada"),

    /** El movimiento ya tiene una novedad sin resolver. */
    PENDING_NEWS_EXISTS(
            "El movimiento ya tiene una novedad pendiente de autorización"),

    /** El solicitante de la novedad no puede autorizarla. */
    SAME_USER_APPROVAL(
            "El usuario que solicita la novedad no puede autorizarla"),

    /** Falla al acceder a la base de datos de novedades. */
    DATABASE_ACCESS_ERROR(
            "Error al acceder a la información de novedades de movimientos");

    private final String message;

    IndividualNewsMessage(String message) {
        this.message = message;
    }

    public String getMessage() {
        return message;
    }
}