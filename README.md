package co.com.bnpparibas.cardif.closingclaims.domain.entity;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Entity
@Table(name = "historicomovimientos", schema = "dbo")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ClaimMovementHistory {

    @Id
    @Column(name = "idcarvajal")
    private Long idCarvajal;

    @Column(name = "socio")
    private String socio;

    @Column(name = "numerosiniestro")
    private String numeroSiniestro;

    @Column(name = "nroidentificacion")
    private String nroIdentificacion;

    @Column(name = "codproducto")
    private String codProducto;

    @Column(name = "codplan")
    private String codPlan;

    @Column(name = "cobertura")
    private String cobertura;

    @Column(name = "ramo")
    private String ramo;

    @Column(name = "vrmovimiento")
    private BigDecimal vrMovimiento;

    @Column(name = "fechamovimiento2")
    private LocalDateTime fechaMovimiento2;

    @Column(name = "tipomovimiento")
    private String tipoMovimiento;

    @Column(name = "fechanacimiento")
    private LocalDateTime fechaNacimiento;

    @Column(name = "fechaocurrencia")
    private LocalDateTime fechaOcurrencia;

    @Column(name = "fechaavisosocio")
    private LocalDateTime fechaAvisoSocio;

    @Column(name = "fechaavisocardif")
    private LocalDateTime fechaAvisoCardif;

    @Column(name = "beneficiariopago")
    private String beneficiarioPago;

    @Column(name = "codsocio")
    private Integer codSocio;

    @Column(name = "idcardif")
    private String idCardif;

    @Column(name = "llavesiniestro")
    private String llaveSiniestro;

    @Column(name = "estadosiniestro")
    private String estadoSiniestro;

    @Column(name = "estadomayor")
    private String estadoMayor;

    @Column(name = "canal")
    private String canal;

    @Column(name = "pandemia")
    private String pandemia;

    @Column(name = "tipocoaseguro")
    private Integer tipoCoaseguro;

    @Column(name = "vrcoaseguroretenido")
    private Double vrCoaseguroRetenido;

    @Column(name = "vrcoasegurocedido")
    private Double vrCoaseguroCedido;
}