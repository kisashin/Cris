package co.com.bnpparibas.cardif.closingclaims.domain.util.anums;

/**
 * Estados posibles de una novedad individual de movimientos.
 */
public enum NewsStatus {

    /** La novedad está pendiente de autorización. */
    PENDIENTE,

    /** La novedad fue aplicada sobre el histórico de movimientos. */
    PROCESADO,

    /** La novedad fue cancelada y no se aplicará. */
    CANCELADO
}