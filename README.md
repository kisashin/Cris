package co.com.bnpparibas.cardif.closingclaims.domain.dtos.individualnews;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.math.BigDecimal;
import java.time.LocalDateTime;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;

class IndividualNewsDTOsTest {

    private static final LocalDateTime DATE = LocalDateTime.of(2026, 5, 10, 0, 0);

    @Test
    @DisplayName("ClaimMovementResponseDTO expone los valores del builder")
    void claimMovementResponseDTOBuilderAssignsValues() {
        ClaimMovementResponseDTO dto = ClaimMovementResponseDTO.builder()
                .idCarvajal(100L)
                .claimNumber("SIN-1")
                .identificationNumber("123")
                .productCode("2011")
                .planCode("PLAN")
                .coverage("COBERTURA")
                .branchCode("0001")
                .movementValue(BigDecimal.ONE)
                .movementDate(DATE)
                .movementType("PAGO")
                .partner("SOCIO")
                .cardifId("IDC")
                .claimKey("LLAVE")
                .partnerCode(10)
                .claimStatus("ABIERTO")
                .majorStatus("ANALISIS")
                .channel("CANAL")
                .pandemic("NO")
                .paymentBeneficiary("BENEFICIARIO")
                .coinsuranceType(1)
                .retainedCoinsuranceValue(5.0)
                .cededCoinsuranceValue(2.0)
                .birthDate(DATE)
                .occurrenceDate(DATE)
                .partnerNoticeDate(DATE)
                .cardifNoticeDate(DATE)
                .build();

        assertEquals(100L, dto.getIdCarvajal());
        assertEquals("SIN-1", dto.getClaimNumber());
        assertEquals("123", dto.getIdentificationNumber());
        assertEquals("2011", dto.getProductCode());
        assertEquals("PLAN", dto.getPlanCode());
        assertEquals("COBERTURA", dto.getCoverage());
        assertEquals("0001", dto.getBranchCode());
        assertEquals(BigDecimal.ONE, dto.getMovementValue());
        assertEquals(DATE, dto.getMovementDate());
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
        assertEquals(DATE, dto.getBirthDate());
        assertEquals(DATE, dto.getOccurrenceDate());
        assertEquals(DATE, dto.getPartnerNoticeDate());
        assertEquals(DATE, dto.getCardifNoticeDate());
    }

    @Test
    @DisplayName("ClaimMovementResponseDTO acepta asignacion por setters")
    void claimMovementResponseDTOSettersAssignValues() {
        ClaimMovementResponseDTO dto = new ClaimMovementResponseDTO();

        dto.setIdCarvajal(200L);
        dto.setClaimNumber("SIN-2");
        dto.setMovementType("AJUSTE");

        assertEquals(200L, dto.getIdCarvajal());
        assertEquals("SIN-2", dto.getClaimNumber());
        assertEquals("AJUSTE", dto.getMovementType());
    }

    @Test
    @DisplayName("IndividualNewsRequestDTO expone los valores del builder")
    void individualNewsRequestDTOBuilderAssignsValues() {
        IndividualNewsRequestDTO dto = IndividualNewsRequestDTO.builder()
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
                .birthDate(DATE)
                .occurrenceDate(DATE)
                .partnerNoticeDate(DATE)
                .cardifNoticeDate(DATE)
                .build();

        assertEquals(100L, dto.getIdCarvajal());
        assertEquals("AJUSTE", dto.getMovementType());
        assertEquals("SOCIO", dto.getPartner());
        assertEquals("COBERTURA", dto.getCoverage());
        assertEquals("IDC", dto.getCardifId());
        assertEquals("LLAVE", dto.getClaimKey());
        assertEquals("0002", dto.getBranchCode());
        assertEquals("SIN-1", dto.getClaimNumber());
        assertEquals(Integer.valueOf(20), dto.getPartnerCode());
        assertEquals("CERRADO", dto.getClaimStatus());
        assertEquals("PAGADO", dto.getMajorStatus());
        assertEquals("CANAL", dto.getChannel());
        assertEquals("SI", dto.getPandemic());
        assertEquals("Justificacion", dto.getJustification());
        assertEquals("BENEFICIARIO", dto.getPaymentBeneficiary());
        assertEquals(Integer.valueOf(2), dto.getCoinsuranceType());
        assertEquals(Double.valueOf(200.0), dto.getRetainedCoinsuranceValue());
        assertEquals(Double.valueOf(75.0), dto.getCededCoinsuranceValue());
        assertEquals(DATE, dto.getBirthDate());
        assertEquals(DATE, dto.getOccurrenceDate());
        assertEquals(DATE, dto.getPartnerNoticeDate());
        assertEquals(DATE, dto.getCardifNoticeDate());
    }

    @Test
    @DisplayName("IndividualNewsRequestDTO acepta asignacion por setters")
    void individualNewsRequestDTOSettersAssignValues() {
        IndividualNewsRequestDTO dto = new IndividualNewsRequestDTO();

        dto.setIdCarvajal(300L);
        dto.setJustification("Otra justificacion");
        dto.setCoinsuranceType(3);

        assertEquals(300L, dto.getIdCarvajal());
        assertEquals("Otra justificacion", dto.getJustification());
        assertEquals(Integer.valueOf(3), dto.getCoinsuranceType());
    }

    @Test
    @DisplayName("IndividualNewsDeleteRequestDTO expone los valores del builder")
    void individualNewsDeleteRequestDTOBuilderAssignsValues() {
        IndividualNewsDeleteRequestDTO dto = IndividualNewsDeleteRequestDTO.builder()
                .idCarvajal(100L)
                .justification("Movimiento duplicado")
                .build();

        assertEquals(100L, dto.getIdCarvajal());
        assertEquals("Movimiento duplicado", dto.getJustification());
    }

    @Test
    @DisplayName("IndividualNewsDeleteRequestDTO acepta asignacion por setters")
    void individualNewsDeleteRequestDTOSettersAssignValues() {
        IndividualNewsDeleteRequestDTO dto = new IndividualNewsDeleteRequestDTO();

        dto.setIdCarvajal(400L);
        dto.setJustification("Registro erroneo");

        assertEquals(400L, dto.getIdCarvajal());
        assertEquals("Registro erroneo", dto.getJustification());
    }

    @Test
    @DisplayName("IndividualNewsResponseDTO expone los valores del builder")
    void individualNewsResponseDTOBuilderAssignsValues() {
        IndividualNewsResponseDTO dto = IndividualNewsResponseDTO.builder()
                .code(55L)
                .idCarvajal(100L)
                .claimNumber("SIN-1")
                .newsType("ACTUALIZA")
                .status("PENDIENTE")
                .justification("Justificacion")
                .processDate(DATE)
                .requestUser("f93141")
                .authorizerUser("f00999")
                .build();

        assertEquals(55L, dto.getCode());
        assertEquals(100L, dto.getIdCarvajal());
        assertEquals("SIN-1", dto.getClaimNumber());
        assertEquals("ACTUALIZA", dto.getNewsType());
        assertEquals("PENDIENTE", dto.getStatus());
        assertEquals("Justificacion", dto.getJustification());
        assertEquals(DATE, dto.getProcessDate());
        assertEquals("f93141", dto.getRequestUser());
        assertEquals("f00999", dto.getAuthorizerUser());
    }

    @Test
    @DisplayName("IndividualNewsResponseDTO acepta asignacion por setters")
    void individualNewsResponseDTOSettersAssignValues() {
        IndividualNewsResponseDTO dto = new IndividualNewsResponseDTO();

        dto.setCode(66L);
        dto.setStatus("CANCELADO");
        dto.setAuthorizerUser("f22222");

        assertEquals(66L, dto.getCode());
        assertEquals("CANCELADO", dto.getStatus());
        assertEquals("f22222", dto.getAuthorizerUser());
    }

    @Test
    @DisplayName("Los DTO exponen el constructor sin argumentos usado por Jackson")
    void dtosExposeNoArgsConstructor() {
        assertNotNull(new ClaimMovementResponseDTO());
        assertNotNull(new IndividualNewsRequestDTO());
        assertNotNull(new IndividualNewsDeleteRequestDTO());
        assertNull(new IndividualNewsResponseDTO().getCode());
    }
}