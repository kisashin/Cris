package co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;

/**
 * Fila del reporte mensual de Aval.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AvalReportRow {

    private String compania;
    private String sucursal;
    private String descripcionRamo;
    private String symbol;
    private Integer ramo2;
    private String nroPoliza;
    private String modulo;
    private String codBancoNegocio;
    private String descripcionTomador;
    private String polizaLiderAlfa;
    private String siniestroLider;
    private Integer valor;
    private Integer numeroLote;
    private String campoUnion;
    private BigDecimal valorInicialReserva;
    private BigDecimal valorAjustesReserva;
    private BigDecimal valorPagos;
    private BigDecimal valorActualReserva;
    private Integer porcentajeAlfa;
    private Integer valorGastosCoaseguro;
    private Integer valorSalvamento;
    private Integer valorRecuperaciones;
    private String nroidentificacion;
    private String nombreasegurado;
    private String fechanacimiento;
    private Integer edad;
    private String sexo;
    private String profesion;
    private String fechaperdida;
    private String fechaaviso;
    private String fechareclamo;
    private String codigoCausa;
    private String causaSiniestro;
    private String ciudad;
    private String tipoSiniestro;
    private String nroCredito;
    private String fechadesembolso;
    private String porcentajeAsegurabilidad;
    private String tipocredito;
    private String coberturaLider;
    private String reportadoPor;
    private String nitBeneficiario;
    private String beneficiario;
    private String causalObjecion;
    private String fechaObjecion;
    private String placa;
    private String serial;
    private String motor;
    private String tipoVehiculo;
    private String claseVehiculo;
    private String observacionesPago;
}
