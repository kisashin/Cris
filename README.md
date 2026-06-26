CardifCenterClosing

package co.com.bnpparibas.cardif.closingclaims.domain.entity;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.hibernate.annotations.Immutable;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;
import java.io.Serializable;
import java.math.BigDecimal;

/**
 * Entidad de solo lectura que representa la vista {@code dbo.vw_mov_cardif_cen}.
 *
 * <p>Corresponde al reporte de movimientos de la pantalla legacy
 * "Cierre Cardif Centroamérica" ({@code AsientoCardifCentro.aspx.vb}). No confundir con
 * el módulo {@code PeruAccountingReport}, que mapea otra tabla
 * ({@code reportecontable_peru}).</p>
 *
 * <p>La vista entrega TODAS las fechas y varios identificadores como texto
 * ({@code varchar}); por eso casi todos los campos son {@code String}.
 * {@code Valordeuda} y {@code Valoraseguradototal} son {@code float}
 * ({@code Double}). A diferencia del módulo de Perú, en Centroamérica
 * {@code Vrmovimiento} es {@code decimal(38,2)}, por lo que se mapea a
 * {@code BigDecimal} para no perder precisión contable. La llave
 * {@code IDCARVAJAL} es {@code bigint} y única por fila, por lo que se usa
 * como identificador simple.</p>
 *
 * <p>Marcada como {@link Immutable} porque es una vista: la aplicación solo la
 * lee, nunca la escribe.</p>
 */
@Entity
@Immutable
@Table(name = "vw_mov_cardif_cen")
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CardifCenterClosing implements Serializable {

    private static final long serialVersionUID = 1L;

    @Id
    @Column(name = "IDCARVAJAL")
    private Long idCarvajal;

    @Column(name = "Socio")
    private String partner;

    @Column(name = "NumeroSiniestro")
    private String claimNumber;

    @Column(name = "Nroidentificacion")
    private String identificationNumber;

    @Column(name = "Tipodocumento")
    private String documentType;

    @Column(name = "Fechanacimiento")
    private String birthDate;

    @Column(name = "Genero")
    private String gender;

    @Column(name = "Direccion")
    private String address;

    @Column(name = "Ciudad")
    private String city;

    @Column(name = "Telefono")
    private String phone;

    @Column(name = "Celular")
    private String mobilePhone;

    @Column(name = "Actividad")
    private String activity;

    @Column(name = "Nomproducto")
    private String productName;

    @Column(name = "Codproducto")
    private String productCode;

    @Column(name = "CodPlan")
    private String planCode;

    @Column(name = "Cobertura")
    private String coverage;

    @Column(name = "Ramo")
    private String branch;

    @Column(name = "Cuotasapagar")
    private Integer installmentsToPay;

    @Column(name = "Certificado")
    private String certificate;

    @Column(name = "Fechainiciovigencia")
    private String policyStartDate;

    @Column(name = "Fechaocurrencia")
    private String occurrenceDate;

    @Column(name = "Fechaavisosocio")
    private String partnerNoticeDate;

    @Column(name = "Fechaavisocardif")
    private String cardifNoticeDate;

    @Column(name = "Valordeuda")
    private Double debtValue;

    @Column(name = "Valoraseguradototal")
    private Double totalInsuredValue;

    @Column(name = "Fechasistematizacion")
    private String systematizationDate;

    @Column(name = "Fecharecepmiddle")
    private String middleReceptionDate;

    @Column(name = "Fecharecepback")
    private String backReceptionDate;

    @Column(name = "Fechaconfcartera")
    private String portfolioConfirmationDate;

    @Column(name = "Causaobjecion")
    private String objectionReason;

    @Column(name = "Fechaenviocartaobj")
    private String objectionLetterSentDate;

    @Column(name = "Causalsuspenso")
    private String suspenseReason;

    @Column(name = "Fechamovimiento")
    private String movementDate;

    @Column(name = "Vrmovimiento")
    private BigDecimal movementValue;

    @Column(name = "Beneficiariopago")
    private String paymentBeneficiary;

    @Column(name = "Pagocomercial")
    private String commercialPayment;

    @Column(name = "Fechaentregaultdocto")
    private String lastDocumentDeliveryDate;

    @Column(name = "Iddoctosoportemanutencion")
    private String maintenanceSupportDocumentId;

    @Column(name = "Codsocio")
    private Integer partnerCode;

    @Column(name = "Analista")
    private String analyst;

    @Column(name = "Nopoliza")
    private String policyNumber;

    @Column(name = "Idcardif")
    private String cardifId;

    @Column(name = "Llavesiniestro")
    private String claimKey;

    @Column(name = "Nombreasegurado")
    private String insuredName;

    @Column(name = "Edad")
    private Integer age;

    @Column(name = "Estadosiniestro")
    private String claimStatus;

    @Column(name = "Estadomayor")
    private String majorStatus;

    @Column(name = "Fechaestadosiniestro")
    private String claimStatusDate;

    @Column(name = "Tipomovimiento")
    private String movementType;

    @Column(name = "Conceptopago")
    private String paymentConcept;

    @Column(name = "Informacion")
    private String information;

    @Column(name = "Baseorigen")
    private String sourceBase;

    @Column(name = "Anomovimiento")
    private Integer movementYear;

    @Column(name = "Mesmovimiento")
    private Integer movementMonth;

    @Column(name = "Diamovimiento")
    private Integer movementDay;

    @Column(name = "Anomessist")
    private String systemYearMonth;

    @Column(name = "Anosist")
    private Integer systemYear;

    @Column(name = "Messist")
    private Integer systemMonth;

    @Column(name = "Agrupacionmov")
    private String movementGrouping;

    @Column(name = "Tipopago")
    private String paymentType;

    @Column(name = "Fechadesembolso")
    private String disbursementDate;

    @Column(name = "Clasepago")
    private String paymentClass;

    @Column(name = "Estadopagoprog")
    private String scheduledPaymentStatus;

    @Column(name = "Vrcuotaplan")
    private String planInstallmentValue;

    @Column(name = "Estadosiniestro2")
    private String claimStatusTwo;

    @Column(name = "Estadomayor2")
    private String majorStatusTwo;

    @Column(name = "Fechaestadosiniestro2")
    private String claimStatusDateTwo;

    @Column(name = "Fechaentregaultdocto2")
    private String lastDocumentDeliveryDateTwo;

    @Column(name = "Fechamovimiento2")
    private String movementDateTwo;

    @Column(name = "Fechacontabilizacion")
    private String accountingDate;

    @Column(name = "vrReaseguroRetenido")
    private String retainedReinsuranceValue;

    @Column(name = "Moneda")
    private String currency;
}
