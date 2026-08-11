package co.com.bnpparibas.cardif.closingclaims.domain.util.helpers;

import co.com.bnpparibas.cardif.closingclaims.domain.dtos.individualnews.ClaimMovementResponseDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.individualnews.IndividualNewsRequestDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.individualnews.IndividualNewsResponseDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.entity.ClaimMovementHistory;
import co.com.bnpparibas.cardif.closingclaims.domain.entity.IndividualNewsHistory;
import co.com.bnpparibas.cardif.closingclaims.domain.util.anums.NewsStatus;
import co.com.bnpparibas.cardif.closingclaims.domain.util.anums.NewsType;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.Collections;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;

class IndividualNewsMapperTest {

    private static final LocalDateTime BIRTH_DATE = LocalDateTime.of(1980, 1, 1, 0, 0);
    private static final LocalDateTime OCCURRENCE_DATE = LocalDateTime.of(2026, 1, 5, 0, 0);

    @Test
    @DisplayName("toMovementResponseDTO traduce todos los campos del movimiento")
    void toMovementResponseDTOMapsAllFields() {
        ClaimMovementHistory entity = ClaimMovementHistory.builder()
                .idCarvajal(100L)
                .socio("SOCIO")
                .numeroSiniestro("SIN-1")
                .nroIdentificacion("123")
                .codProducto("2011")
                .codPlan("PLAN")
                .cobertura("COBERTURA")
                .ramo("0001")
                .vrMovimiento(new BigDecimal("10.25"))
                .fechaMovimiento2(OCCURRENCE_DATE)
                .tipoMovimiento("PAGO")
                .fechaNacimiento(BIRTH_DATE)
                .fechaOcurrencia(OCCURRENCE_DATE)
                .fechaAvisoSocio(OCCURRENCE_DATE)
                .fechaAvisoCardif(OCCURRENCE_DATE)
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

        ClaimMovementResponseDTO dto = IndividualNewsMapper.INSTANCE
                .toMovementResponseDTO(entity);

        assertEquals(100L, dto.getIdCarvajal());
        assertEquals("SIN-1", dto.getClaimNumber());
        assertEquals("123", dto.getIdentificationNumber());
        assertEquals("2011", dto.getProductCode());
        assertEquals("PLAN", dto.getPlanCode());
        assertEquals("COBERTURA", dto.getCoverage());
        assertEquals("0001", dto.getBranchCode());
        assertEquals(new BigDecimal("10.25"), dto.getMovementValue());
        assertEquals(OCCURRENCE_DATE, dto.getMovementDate());
        assertEquals("PAGO", dto.getMovementType());
        assertEquals("SOCIO", dto.getPartner());
        assertEquals("IDC", dto.getCardifId());
        assertEquals("LLAVE", dto.getClaimKey());
        assertEquals(Integer.valueOf(10), dto.getPartnerCode());
        assertEquals("ABIERTO", dto.getClaimStatus());
        assertEquals("ANALISIS", dto.getMajorStatus());
        assertEquals("CANAL", dto.getChannel());
        assertEquals("NO", dto.getPandemic());
        assertEquals("BENEFICIARIO", dto.getPaymentBeneficiary());
        assertEquals(Integer.valueOf(1), dto.getCoinsuranceType());
        assertEquals(Double.valueOf(5.0), dto.getRetainedCoinsuranceValue());
        assertEquals(Double.valueOf(2.0), dto.getCededCoinsuranceValue());
        assertEquals(BIRTH_DATE, dto.getBirthDate());
    }

    @Test
    @DisplayName("toMovementResponseDTO retorna nulo cuando la entidad es nula")
    void toMovementResponseDTOReturnsNullForNullEntity() {
        assertNull(IndividualNewsMapper.INSTANCE.toMovementResponseDTO(null));
    }

    @Test
    @DisplayName("toMovementResponseDTOList traduce la coleccion completa")
    void toMovementResponseDTOListMapsCollection() {
        ClaimMovementHistory entity = ClaimMovementHistory.builder()
                .idCarvajal(100L)
                .numeroSiniestro("SIN-1")
                .build();

        List<ClaimMovementResponseDTO> result = IndividualNewsMapper.INSTANCE
                .toMovementResponseDTOList(Collections.singletonList(entity));

        assertEquals(1, result.size());
        assertEquals("SIN-1", result.get(0).getClaimNumber());
    }

    @Test
    @DisplayName("toMovementResponseDTOList retorna nulo cuando la lista es nula")
    void toMovementResponseDTOListReturnsNullForNullList() {
        assertNull(IndividualNewsMapper.INSTANCE.toMovementResponseDTOList(null));
    }

    @Test
    @DisplayName("toNewsResponseDTO traduce los enums a texto")
    void toNewsResponseDTOMapsEnumsToText() {
        IndividualNewsHistory entity = IndividualNewsHistory.builder()
                .codigo(55L)
                .idCarvajal(100L)
                .numeroSiniestro("SIN-1")
                .observacion("Justificacion")
                .estado(NewsStatus.PENDIENTE)
                .tipoNovedad(NewsType.ELIMINA)
                .fechaProceso(OCCURRENCE_DATE)
                .idUsuario("f93141")
                .idAutorizador("f00999")
                .build();

        IndividualNewsResponseDTO dto = IndividualNewsMapper.INSTANCE
                .toNewsResponseDTO(entity);

        assertEquals(55L, dto.getCode());
        assertEquals(100L, dto.getIdCarvajal());
        assertEquals("SIN-1", dto.getClaimNumber());
        assertEquals(NewsStatus.PENDIENTE.name(), dto.getStatus());
        assertEquals(NewsType.ELIMINA.name(), dto.getNewsType());
        assertEquals("Justificacion", dto.getJustification());
        assertEquals(OCCURRENCE_DATE, dto.getProcessDate());
        assertEquals("f93141", dto.getRequestUser());
        assertEquals("f00999", dto.getAuthorizerUser());
    }

    @Test
    @DisplayName("toNewsResponseDTO retorna nulo cuando la entidad es nula")
    void toNewsResponseDTOReturnsNullForNullEntity() {
        assertNull(IndividualNewsMapper.INSTANCE.toNewsResponseDTO(null));
    }

    @Test
    @DisplayName("toNewsResponseDTOList traduce la coleccion completa")
    void toNewsResponseDTOListMapsCollection() {
        IndividualNewsHistory entity = IndividualNewsHistory.builder()
                .codigo(55L)
                .estado(NewsStatus.CANCELADO)
                .build();

        List<IndividualNewsResponseDTO> result = IndividualNewsMapper.INSTANCE
                .toNewsResponseDTOList(Collections.singletonList(entity));

        assertEquals(1, result.size());
        assertEquals(NewsStatus.CANCELADO.name(), result.get(0).getStatus());
    }

    @Test
    @DisplayName("toNewsResponseDTOList retorna nulo cuando la lista es nula")
    void toNewsResponseDTOListReturnsNullForNullList() {
        assertNull(IndividualNewsMapper.INSTANCE.toNewsResponseDTOList(null));
    }

    @Test
    @DisplayName("toEntity traduce la solicitud y deja los campos de control sin asignar")
    void toEntityMapsRequestAndIgnoresControlFields() {
        IndividualNewsRequestDTO request = IndividualNewsRequestDTO.builder()
                .idCarvajal(100L)
                .movementType("AJUSTE")
                .partner("SOCIO")
                .coverage("COBERTURA")
                .cardifId("IDC")
                .claimKey("LLAVE")
                .branchCode("0002")
                .claimNumber("SIN-1")
                .partnerCode(20)
                .claimStatus("CERRADO")
                .majorStatus("PAGADO")
                .channel("CANAL")
                .pandemic("SI")
                .justification("Justificacion")
                .paymentBeneficiary("BENEFICIARIO")
                .coinsuranceType(2)
                .retainedCoinsuranceValue(200.0)
                .cededCoinsuranceValue(75.0)
                .birthDate(BIRTH_DATE)
                .occurrenceDate(OCCURRENCE_DATE)
                .partnerNoticeDate(OCCURRENCE_DATE)
                .cardifNoticeDate(OCCURRENCE_DATE)
                .build();

        IndividualNewsHistory entity = IndividualNewsMapper.INSTANCE.toEntity(request);

        assertNotNull(entity);
        assertEquals(100L, entity.getIdCarvajal());
        assertEquals("SOCIO", entity.getSocio());
        assertEquals("SIN-1", entity.getNumeroSiniestro());
        assertEquals("COBERTURA", entity.getCobertura());
        assertEquals("0002", entity.getRamo());
        assertEquals("IDC", entity.getIdCardif());
        assertEquals("LLAVE", entity.getLlaveSiniestro());
        assertEquals(Integer.valueOf(20), entity.getCodSocio());
        assertEquals("CERRADO", entity.getEstadoSiniestro());
        assertEquals("PAGADO", entity.getEstadoMayor());
        assertEquals("AJUSTE", entity.getTipoMovimiento());
        assertEquals("CANAL", entity.getCanal());
        assertEquals("SI", entity.getPandemia());
        assertEquals("BENEFICIARIO", entity.getBeneficiarioPago());
        assertEquals(Integer.valueOf(2), entity.getTipoCoaseguro());
        assertEquals(Double.valueOf(200.0), entity.getVrCoaseguroRetenido());
        assertEquals(Double.valueOf(75.0), entity.getVrCoaseguroCedido());
        assertEquals("Justificacion", entity.getObservacion());
        assertEquals(BIRTH_DATE, entity.getFechaNacimiento());
        assertEquals(OCCURRENCE_DATE, entity.getFechaOcurrencia());
        assertNull(entity.getCodigo());
        assertNull(entity.getEstado());
        assertNull(entity.getTipoNovedad());
        assertNull(entity.getFechaProceso());
        assertNull(entity.getIdUsuario());
        assertNull(entity.getIdAutorizador());
    }

    @Test
    @DisplayName("toEntity retorna nulo cuando la solicitud es nula")
    void toEntityReturnsNullForNullRequest() {
        assertNull(IndividualNewsMapper.INSTANCE.toEntity(null));
    }
}