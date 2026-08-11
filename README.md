package co.com.bnpparibas.cardif.closingclaims.domain.entity;

import co.com.bnpparibas.cardif.closingclaims.domain.util.anums.NewsStatus;
import co.com.bnpparibas.cardif.closingclaims.domain.util.anums.NewsType;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.EnumType;
import javax.persistence.Enumerated;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Table;
import java.time.LocalDateTime;

@Entity
@Table(name = "novedadhistoricoindividual", schema = "dbo")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class IndividualNewsHistory {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "codigo")
    private Long codigo;

    @Column(name = "id", nullable = false)
    private Long idCarvajal;

    @Column(name = "socio")
    private String socio;

    @Column(name = "numerosiniestro")
    private String numeroSiniestro;

    @Column(name = "fechanacimiento")
    private LocalDateTime fechaNacimiento;

    @Column(name = "cobertura")
    private String cobertura;

    @Column(name = "ramo")
    private String ramo;

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

    @Column(name = "tipomovimiento")
    private String tipoMovimiento;

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

    @Column(name = "observacion")
    private String observacion;

    @Enumerated(EnumType.STRING)
    @Column(name = "estado")
    private NewsStatus estado;

    @Enumerated(EnumType.STRING)
    @Column(name = "tiponovedad")
    private NewsType tipoNovedad;

    @Column(name = "fechaproceso")
    private LocalDateTime fechaProceso;

    @Column(name = "idusuario")
    private String idUsuario;

    @Column(name = "idautorizador")
    private String idAutorizador;
}