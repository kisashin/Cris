PeruAccountingReport

package co.com.bnpparibas.cardif.closingclaims.domain.entity;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import javax.persistence.Column;
import javax.persistence.EmbeddedId;
import javax.persistence.Entity;
import javax.persistence.Table;
import java.io.Serializable;
import java.time.LocalDateTime;

/**
 * Entidad que representa la tabla {@code reportecontable_peru}.
 *
 * <p>La tabla no posee una llave primaria física, por lo que se utiliza
 * una llave lógica compuesta definida en {@link PeruAccountingReportId}.</p>
 */
@Entity
@Table(name = "reportecontable_peru")
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class PeruAccountingReport implements Serializable {

    private static final long serialVersionUID = 1L;

    /**
     * Identificador lógico compuesto.
     */
    @EmbeddedId
    private PeruAccountingReportId id;

    @Column(name = "FechaAviso")
    private String noticeDate;

    @Column(name = "MesNotificacion")
    private String notificationMonth;

    @Column(name = "FechaAvisoCardif")
    private String cardifNoticeDate;

    @Column(name = "FechaAvisoSocio")
    private String partnerNoticeDate;

    @Column(name = "FechaUltDocRecCardif")
    private String lastDocumentReceivedDate;

    @Column(name = "FechaPublicacion")
    private String publicationDate;

    @Column(name = "Socio")
    private String partner;

    @Column(name = "Producto")
    private String product;

    @Column(name = "CodProducto")
    private Double productCode;

    @Column(name = "Certificado")
    private String certificate;

    @Column(name = "FechaInicioPoliza")
    private String policyStartDate;

    @Column(name = "FechaFinPoliza")
    private String policyEndDate;

    @Column(name = "ValidacionEdadIngreso")
    private String entryAgeValidation;

    @Column(name = "ValidacionEdadPermanencia")
    private String permanenceAgeValidation;

    @Column(name = "ValidacionCarencia")
    private String waitingPeriodValidation;

    @Column(name = "FechaOcurrencia")
    private String occurrenceDate;

    @Column(name = "MesOcurrencia")
    private String occurrenceMonth;

    @Column(name = "TipoDocAsegurado")
    private String insuredDocumentType;

    @Column(name = "NroDocAsegurado")
    private String insuredDocumentNumber;

    @Column(name = "NombreAsegurado")
    private String insuredName;

    @Column(name = "ControlDuplicidad")
    private String duplicationControl;

    @Column(name = "Genero")
    private String gender;

    @Column(name = "Nacionalidad")
    private String nationality;

    @Column(name = "FechaNacto")
    private String birthDate;

    @Column(name = "EdadFecOcurrencia")
    private String ageAtOccurrenceDate;

    @Column(name = "CoberturaAfectada")
    private String affectedCoverage;

    @Column(name = "Moneda")
    private String currency;

    @Column(name = "ReservaInicial")
    private Double initialReserve;

    @Column(name = "PagoReal")
    private Double actualPayment;

    @Column(name = "SaldoReserva")
    private Double reserveBalance;

    @Column(name = "EstadoSiniestro2")
    private String claimStatus;

    @Column(name = "EstadoMayor")
    private String majorStatus;

    @Column(name = "FechaRegTransaccion")
    private String transactionRegistrationDate;

    @Column(name = "MesAprobacionRechazo")
    private String approvalRejectionMonth;

    @Column(name = "Cie10")
    private String cie10;

    @Column(name = "Diagnostico")
    private String diagnosis;

    @Column(name = "MotivoRechazo")
    private String rejectionReason;

    @Column(name = "MotivoRechazoAgrupado")
    private Double groupedRejectionReason;

    @Column(name = "NroPlanilla")
    private String payrollNumber;

    @Column(name = "NroCarta")
    private String letterNumber;

    @Column(name = "Observaciones")
    private String observations;

    @Column(name = "Resumen")
    private String summary;

    @Column(name = "Ubicacion")
    private String location;

    @Column(name = "FechaEntregaLiquiContab")
    private String accountingSettlementDeliveryDate;

    @Column(name = "FechaEmiCheque")
    private String checkIssueDate;

    @Column(name = "FechaEntrCheque")
    private String checkDeliveryDate;

    @Column(name = "ValorMaxCuota")
    private String maximumInstallmentValue;

    @Column(name = "NumeroCuota")
    private String installmentNumber;

    @Column(name = "Plan1")
    private String planOne;

    @Column(name = "EjecutivoCAFAE")
    private String cafaeExecutive;

    @Column(name = "RefCAFAE")
    private String cafaeReference;

    @Column(name = "Parentesco")
    private String relationship;

    @Column(name = "[Contrato/Expediente]")
    private String contractOrFile;

    @Column(name = "EjecutivoCAFAE2")
    private String secondaryCafaeExecutive;

    @Column(name = "Parentesco1")
    private String secondaryRelationship;

    @Column(name = "Plan2")
    private String planTwo;

    @Column(name = "TipoDocBeneficiario")
    private String beneficiaryDocumentType;

    @Column(name = "NroDocBeneficiario")
    private String beneficiaryDocumentNumber;

    @Column(name = "Parentesco2")
    private String beneficiaryRelationship;

    @Column(name = "FondoCAFAE")
    private String cafaeFund;

    @Column(name = "DiasCN")
    private String cnDays;

    @Column(name = "DiasUCI")
    private String intensiveCareDays;

    @Column(name = "CalculoLiquidacion")
    private String settlementCalculation;

    @Column(name = "SucursalRetiro")
    private String withdrawalBranch;

    @Column(name = "Celular")
    private String mobilePhone;

    @Column(name = "Cartera")
    private String wallet;

    @Column(name = "Maletin")
    private String briefcase;

    @Column(name = "Billetera")
    private String billfold;

    @Column(name = "PortaDcmtos")
    private String documentHolder;

    @Column(name = "LentesOpticos")
    private String opticalGlasses;

    @Column(name = "LentesSol")
    private String sunglasses;

    @Column(name = "Cosmeticos")
    private String cosmetics;

    @Column(name = "Lapicero")
    private String pen;

    @Column(name = "DNI")
    private String nationalIdentityDocument;

    @Column(name = "Mochila")
    private String backpack;

    @Column(name = "Reloj")
    private String watch;

    @Column(name = "DiscIpodMP3Tablet")
    private String electronicDevices;

    @Column(name = "PalmTablet")
    private String palmTablet;

    @Column(name = "Bolso")
    private String bag;

    @Column(name = "SillaAutoBB")
    private String babyCarSeat;

    @Column(name = "CocheBB")
    private String babyStroller;

    @Column(name = "Discos")
    private String discs;

    @Column(name = "Llanta")
    private String tire;

    @Column(name = "GasMedicos")
    private String medicalGases;

    @Column(name = "LibreDispon")
    private String freeAvailability;

    @Column(name = "MuerteAccid")
    private String accidentalDeath;

    @Column(name = "Llaves")
    private String keys;

    @Column(name = "DiasHospitalizacion")
    private String hospitalizationDays;

    @Column(name = "[Excepción]")
    private String exception;

    @Column(name = "TelefonoReferencia")
    private String referencePhone;

    @Column(name = "Contacto")
    private String contact;

    @Column(name = "Correo")
    private String email;

    @Column(name = "Direccion")
    private String address;

    @Column(name = "Departamento")
    private String department;

    @Column(name = "Provincia")
    private String province;

    @Column(name = "Distrito")
    private String district;

    @Column(name = "CodigoRamo")
    private Double branchCode;

    @Column(name = "NroTarjeta")
    private String cardNumber;

    @Column(name = "TipoTarjeta")
    private String cardType;

    @Column(name = "ReasegurosPenCAFAE")
    private String cafaePendingReinsurance;

    @Column(name = "SaldoReservaCoaseguroReaseguros")
    private String coinsuranceReinsuranceReserveBalance;

    @Column(name = "SaldoReservaCoaseguroReaseguroRECH")
    private String rejectedCoinsuranceReinsuranceReserveBalance;

    @Column(name = "CodigoAct")
    private String activityCode;

    @Column(name = "TasaRechazo")
    private String rejectionRate;

    @Column(name = "SaldoReservaTasaRechazo")
    private String rejectionRateReserveBalance;

    @Column(name = "FechaReporte")
    private LocalDateTime reportDate;

    @Column(name = "Pandemia")
    private String pandemic;

    @Column(name = "FamiliaCobertura")
    private String coverageFamily;

    @Column(name = "FechaEnvioCartas")
    private String letterSentDate;

    @Column(name = "DiasIngresos")
    private String entryDays;

    @Column(name = "RangoIngresos")
    private String entryRange;

    @Column(name = "DiasTrascurridosAvisosocio")
    private String partnerNoticeElapsedDays;

    @Column(name = "DiasTrascurridosAvisocardif")
    private String cardifNoticeElapsedDays;

    @Column(name = "RangoAvisosocios")
    private String partnerNoticeRange;

    @Column(name = "RangoAvisocardif")
    private String cardifNoticeRange;

    @Column(name = "CanalIngreso")
    private String entryChannel;

    @Column(name = "RamoProductos")
    private String productBranch;

    @Column(name = "Causalobjecion_scoring")
    private String scoringObjectionReason;
}
