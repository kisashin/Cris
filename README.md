package co.com.bnpparibas.cardif.closingclaims.domain.entity;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import javax.persistence.Column;
import javax.persistence.Embeddable;
import java.io.Serializable;
import java.time.LocalDateTime;

/**
 * Identificador compuesto lógico del reporte contable de Perú.
 *
 * <p>La combinación del número de siniestro y la fecha del movimiento
 * identifica de forma única cada registro.</p>
 */
@Embeddable
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode
public class PeruAccountingReportId implements Serializable {

    private static final long serialVersionUID = 1L;

    /**
     * Número del siniestro.
     */
    @Column(name = "NumeroSiniestro")
    private String claimNumber;

    /**
     * Fecha del movimiento.
     */
    @Column(name = "Fechamovimiento2")
    private LocalDateTime movementDate;
}
