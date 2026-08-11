package co.com.bnpparibas.cardif.closingclaims.domain.entity;

import co.com.bnpparibas.cardif.closingclaims.domain.util.anums.NewsStatus;
import co.com.bnpparibas.cardif.closingclaims.domain.util.anums.NewsType;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.math.BigDecimal;
import java.time.LocalDateTime;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;

class IndividualNewsEntitiesTest {

    private static final LocalDateTime DATE = LocalDateTime.of(2026, 5, 10, 0, 0);

    @Test
    @DisplayName("ClaimMovementHistory expone los valores asignados por el builder")
    void claimMovementHistoryBuilderAssignsValues() {
        ClaimMovementHistory entity = ClaimMovementHistory.builder()
                .idCarvajal(100L)
                .socio("SOCIO")
                .numeroSiniestro("SIN-1")
                .nroIdentificacion("123")
                .codProducto("2011")
                .codPlan("PLAN")
                .cobertura("COBERTURA")
                .ramo("0001")
                .vrMovimiento(BigDecimal.TEN)
                .fechaMovimiento2(DATE)
                .tipoMovimiento("PAGO")
                .fechaNacimiento(DATE)
                .fechaOcurrencia(DATE)
                .fechaAvisoSocio(DATE)
                .fechaAvisoCardif(DATE)
                .beneficiarioPago("BENEFICIARIO")
                .codSocio(10)
                .idCardif("IDC")
                .llaveSiniestro("LLAVE")
                .estadoSiniestro("ABIERTO")
                .estadoMayor("ANALISIS")
                .canal("CANAL")
                .pandemia("NO")
                .tipoCoaseguro(1)
                .vrCoaseguroRetenido(5.0)
                .vrCoaseguroCedido(2.0)
                .build();

        assertEquals(100L, entity.getIdCarvajal());
        assertEquals("SOCIO", entity.getSocio());
        assertEquals("SIN-1", entity.getNumeroSiniestro());
        assertEquals("123", entity.getNroIdentificacion());
        assertEquals("2011", entity.getCodProducto());
        assertEquals("PLAN", entity.getCodPlan());
        assertEquals("COBERTURA", entity.getCobertura());
        assertEquals("0001", entity.getRamo());
        assertEquals(BigDecimal.TEN, entity.getVrMovimiento());
        assertEquals(DATE, entity.getFechaMovimiento2());
        assertEquals("PAGO", entity.getTipoMovimiento());
        assertEquals(DATE, entity.getFechaNacimiento());
        assertEquals(DATE, entity.getFechaOcurrencia());
        assertEquals(DATE, entity.getFechaAvisoSocio());
        assertEquals(DATE, entity.getFechaAvisoCardif());
        assertEquals("BENEFICIARIO", entity.getBeneficiarioPago());
        assertEquals(Integer.valueOf(10), entity.getCodSocio());
        assertEquals("IDC", entity.getIdCardif());
        assertEquals("LLAVE", entity.getLlaveSiniestro());
        assertEquals("ABIERTO", entity.getEstadoSiniestro());
        assertEquals("ANALISIS", entity.getEstadoMayor());
        assertEquals("CANAL", entity.getCanal());
        assertEquals("NO", entity.getPandemia());
        assertEquals(Integer.valueOf(1), entity.getTipoCoaseguro());
        assertEquals(Double.valueOf(5.0), entity.getVrCoaseguroRetenido());
        assertEquals(Double.valueOf(2.0), entity.getVrCoaseguroCedido());
    }

    @Test
    @DisplayName("ClaimMovementHistory acepta asignacion por setters")
    void claimMovementHistorySettersAssignValues() {
        ClaimMovementHistory entity = new ClaimMovementHistory();

        entity.setIdCarvajal(200L);
        entity.setSocio("OTRO SOCIO");
        entity.setNumeroSiniestro("SIN-2");
        entity.setCobertura("OTRA COBERTURA");
        entity.setRamo("0003");
        entity.setTipoMovimiento("AJUSTE");
        entity.setCodSocio(30);
        entity.setTipoCoaseguro(2);
        entity.setVrCoaseguroRetenido(9.0);
        entity.setVrCoaseguroCedido(4.0);

        assertEquals(200L, entity.getIdCarvajal());
        assertEquals("OTRO SOCIO", entity.getSocio());
        assertEquals("SIN-2", entity.getNumeroSiniestro());
        assertEquals("OTRA COBERTURA", entity.getCobertura());
        assertEquals("0003", entity.getRamo());
        assertEquals("AJUSTE", entity.getTipoMovimiento());
        assertEquals(Integer.valueOf(30), entity.getCodSocio());
        assertEquals(Integer.valueOf(2), entity.getTipoCoaseguro());
        assertEquals(Double.valueOf(9.0), entity.getVrCoaseguroRetenido());
        assertEquals(Double.valueOf(4.0), entity.getVrCoaseguroCedido());
    }

    @Test
    @DisplayName("IndividualNewsHistory expone los valores asignados por el builder")
    void individualNewsHistoryBuilderAssignsValues() {
        IndividualNewsHistory entity = IndividualNewsHistory.builder()
                .codigo(55L)
                .idCarvajal(100L)
                .socio("SOCIO")
                .numeroSiniestro("SIN-1")
                .fechaNacimiento(DATE)
                .cobertura("COBERTURA")
                .ramo("0002")
                .fechaOcurrencia(DATE)
                .fechaAvisoSocio(DATE)
                .fechaAvisoCardif(DATE)
                .beneficiarioPago("BENEFICIARIO")
                .codSocio(20)
                .idCardif("IDC")
                .llaveSiniestro("LLAVE")
                .estadoSiniestro("CERRADO")
                .estadoMayor("PAGADO")
                .tipoMovimiento("AJUSTE")
                .canal("CANAL")
                .pandemia("SI")
                .tipoCoaseguro(2)
                .vrCoaseguroRetenido(200.0)
                .vrCoaseguroCedido(75.0)
                .observacion("Justificacion")
                .estado(NewsStatus.PENDIENTE)
                .tipoNovedad(NewsType.ACTUALIZA)
                .fechaProceso(DATE)
                .idUsuario("f93141")
                .idAutorizador("f00999")
                .build();

        assertEquals(55L, entity.getCodigo());
        assertEquals(100L, entity.getIdCarvajal());
        assertEquals("SOCIO", entity.getSocio());
        assertEquals("SIN-1", entity.getNumeroSiniestro());
        assertEquals(DATE, entity.getFechaNacimiento());
        assertEquals("COBERTURA", entity.getCobertura());
        assertEquals("0002", entity.getRamo());
        assertEquals(DATE, entity.getFechaOcurrencia());
        assertEquals(DATE, entity.getFechaAvisoSocio());
        assertEquals(DATE, entity.getFechaAvisoCardif());
        assertEquals("BENEFICIARIO", entity.getBeneficiarioPago());
        assertEquals(Integer.valueOf(20), entity.getCodSocio());
        assertEquals("IDC", entity.getIdCardif());
        assertEquals("LLAVE", entity.getLlaveSiniestro());
        assertEquals("CERRADO", entity.getEstadoSiniestro());
        assertEquals("PAGADO", entity.getEstadoMayor());
        assertEquals("AJUSTE", entity.getTipoMovimiento());
        assertEquals("CANAL", entity.getCanal());
        assertEquals("SI", entity.getPandemia());
        assertEquals(Integer.valueOf(2), entity.getTipoCoaseguro());
        assertEquals(Double.valueOf(200.0), entity.getVrCoaseguroRetenido());
        assertEquals(Double.valueOf(75.0), entity.getVrCoaseguroCedido());
        assertEquals("Justificacion", entity.getObservacion());
        assertEquals(NewsStatus.PENDIENTE, entity.getEstado());
        assertEquals(NewsType.ACTUALIZA, entity.getTipoNovedad());
        assertEquals(DATE, entity.getFechaProceso());
        assertEquals("f93141", entity.getIdUsuario());
        assertEquals("f00999", entity.getIdAutorizador());
    }

    @Test
    @DisplayName("IndividualNewsHistory acepta asignacion por setters")
    void individualNewsHistorySettersAssignValues() {
        IndividualNewsHistory entity = new IndividualNewsHistory();

        entity.setCodigo(66L);
        entity.setIdCarvajal(300L);
        entity.setObservacion("Otra justificacion");
        entity.setEstado(NewsStatus.PROCESADO);
        entity.setTipoNovedad(NewsType.ELIMINA);
        entity.setFechaProceso(DATE);
        entity.setIdUsuario("f11111");
        entity.setIdAutorizador("f22222");

        assertEquals(66L, entity.getCodigo());
        assertEquals(300L, entity.getIdCarvajal());
        assertEquals("Otra justificacion", entity.getObservacion());
        assertEquals(NewsStatus.PROCESADO, entity.getEstado());
        assertEquals(NewsType.ELIMINA, entity.getTipoNovedad());
        assertEquals(DATE, entity.getFechaProceso());
        assertEquals("f11111", entity.getIdUsuario());
        assertEquals("f22222", entity.getIdAutorizador());
    }

    @Test
    @DisplayName("Las entidades exponen el constructor sin argumentos requerido por JPA")
    void entitiesExposeNoArgsConstructor() {
        ClaimMovementHistory movement = new ClaimMovementHistory();
        IndividualNewsHistory news = new IndividualNewsHistory();

        assertNotNull(movement);
        assertNotNull(news);
        assertNull(movement.getIdCarvajal());
        assertNull(news.getCodigo());
    }
}