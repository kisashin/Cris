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
import java.io.Serializable;
import java.math.BigDecimal;
import java.time.LocalDateTime;

/**
 * Representa las columnas exportadas del reporte mensual de Aval.
 */
@Entity
@Table(name = "tmp_repavalcierre")
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class TmpRepAvalCierreReport implements Serializable {

    private static final long serialVersionUID = 1L;

    @Id
    @Column(name = "id")
    private Long id;

    @Column(name = "fechagenera")
    private LocalDateTime fechagenera;

    @Column(name = "compania", length = 2)
    private String compania;

    @Column(name = "sucursal", length = 2)
    private String sucursal;

    @Column(name = "descripcion_ramo", length = 100)
    private String descripcionRamo;

    @Column(name = "symbol", length = 10)
    private String symbol;

    @Column(name = "ramo2")
    private Integer ramo2;

    @Column(name = "nro_poliza", length = 30)
    private String nroPoliza;

    @Column(name = "modulo", length = 2)
    private String modulo;

    @Column(name = "cod_banco_negocio", length = 4)
    private String codBancoNegocio;

    @Column(name = "DESCRIPCION_TOMADOR", length = 20)
    private String descripcionTomador;

    @Column(name = "poliza_lider_alfa", length = 20)
    private String polizaLiderAlfa;

    @Column(name = "SINIESTRO_LIDER", length = 520)
    private String siniestroLider;

    @Column(name = "valor")
    private Integer valor;

    @Column(name = "NUMERO_LOTE")
    private Integer numeroLote;

    @Column(name = "CAMPO_UNION", length = 520)
    private String campoUnion;

    @Column(name = "VALOR_INICIAL_RESERVA")
    private BigDecimal valorInicialReserva;

    @Column(name = "VALOR_AJUSTES_RESERVA")
    private BigDecimal valorAjustesReserva;

    @Column(name = "VALOR_PAGOS")
    private BigDecimal valorPagos;

    @Column(name = "VALOR_ACTUAL_RESERVA")
    private BigDecimal valorActualReserva;

    @Column(name = "PORCENTAJE_ALFA")
    private Integer porcentajeAlfa;

    @Column(name = "VALOR_GASTOS_COASEGURO")
    private Integer valorGastosCoaseguro;

    @Column(name = "VALOR_SALVAMENTO")
    private Integer valorSalvamento;

    @Column(name = "VALOR_RECUPERACIONES")
    private Integer valorRecuperaciones;

    @Column(name = "Nroidentificacion", length = 300)
    private String nroidentificacion;

    @Column(name = "Nombreasegurado", length = 510)
    private String nombreasegurado;

    @Column(name = "fechanacimiento", length = 10)
    private String fechanacimiento;

    @Column(name = "edad")
    private Integer edad;

    @Column(name = "SEXO", length = 2)
    private String sexo;

    @Column(name = "Profesion", length = 510)
    private String profesion;

    @Column(name = "fechaperdida", length = 10)
    private String fechaperdida;

    @Column(name = "fechaaviso", length = 10)
    private String fechaaviso;

    @Column(name = "fechareclamo", length = 10)
    private String fechareclamo;

    @Column(name = "CODIGO_CAUSA", length = 5)
    private String codigoCausa;

    @Column(name = "causa_siniestro", length = 510)
    private String causaSiniestro;

    @Column(name = "ciudad", length = 510)
    private String ciudad;

    @Column(name = "Tipo_siniestro", length = 2)
    private String tipoSiniestro;

    @Column(name = "nro_credito", length = 200)
    private String nroCredito;

    @Column(name = "fechadesembolso", length = 10)
    private String fechadesembolso;

    @Column(name = "porcentaje_asegurabilidad", length = 3)
    private String porcentajeAsegurabilidad;

    @Column(name = "tipocredito", length = 50)
    private String tipocredito;

    @Column(name = "cobertura_lider", length = 510)
    private String coberturaLider;

    @Column(name = "reportado_por", length = 200)
    private String reportadoPor;

    @Column(name = "Nit_beneficiario", length = 20)
    private String nitBeneficiario;

    @Column(name = "Beneficiario", length = 20)
    private String beneficiario;

    @Column(name = "causal_objecion", length = 522)
    private String causalObjecion;

    @Column(name = "fecha_objecion", length = 20)
    private String fechaObjecion;

    @Column(name = "PLACA_", length = 20)
    private String placa;

    @Column(name = "SERIAL_", length = 20)
    private String serial;

    @Column(name = "MOTOR_", length = 20)
    private String motor;

    @Column(name = "TIPO_VEHICULO", length = 20)
    private String tipoVehiculo;

    @Column(name = "CLASE_VEHICULO", length = 20)
    private String claseVehiculo;

    @Column(name = "OBSERVACIONES_PAGO", length = 20)
    private String observacionesPago;
}
