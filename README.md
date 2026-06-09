package co.com.bnpparibas.cardif.closingclaims.domain.dtos.homologation;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;

import javax.validation.ConstraintViolation;
import javax.validation.Validation;
import javax.validation.Validator;
import java.time.LocalDate;
import java.util.Set;

import static org.junit.jupiter.api.Assertions.*;

@ExtendWith(MockitoExtension.class)
class HomologationPolicyDTOsTest {

    private static final LocalDate FECHA_INICIO = LocalDate.of(2024, 1, 1);
    private static final LocalDate FECHA_FIN = LocalDate.of(2024, 12, 31);

    /* ------------------------------------------------------------------ */
    @Test
    @DisplayName("HomologationPolicyRequestDTO - constructor without args and setters")
    void requestDTO_noArgsAndSetters() {
        HomologationPolicyRequestDTO dto = new HomologationPolicyRequestDTO();
        dto.setProductCode(749);
        dto.setBranchCode(31);
        dto.setPolicyNumber("0000490");
        dto.setAppliesValidity(0);
        dto.setStartDate(FECHA_INICIO);
        dto.setEndDate(FECHA_FIN);

        assertAll(
                () -> assertEquals(749, dto.getProductCode()),
                () -> assertEquals(31, dto.getBranchCode()),
                () -> assertEquals("0000490", dto.getPolicyNumber()),
                () -> assertEquals(0, dto.getAppliesValidity()),
                () -> assertEquals(FECHA_INICIO, dto.getStartDate()),
                () -> assertEquals(FECHA_FIN, dto.getEndDate())
        );
    }

    @Test
    @DisplayName("HomologationPolicyRequestDTO - all args constructor")
    void requestDTO_allArgsConstructor() {
        HomologationPolicyRequestDTO dto = new HomologationPolicyRequestDTO(
                749, 31, "0000490", 0, FECHA_INICIO, FECHA_FIN
        );

        assertAll(
                () -> assertEquals(749, dto.getProductCode()),
                () -> assertEquals(31, dto.getBranchCode()),
                () -> assertEquals("0000490", dto.getPolicyNumber()),
                () -> assertEquals(0, dto.getAppliesValidity()),
                () -> assertEquals(FECHA_INICIO, dto.getStartDate()),
                () -> assertEquals(FECHA_FIN, dto.getEndDate())
        );
    }

    @Test
    @DisplayName("HomologationPolicyRequestDTO - null dates are invalid")
    void requestDTO_nullDatesShouldBeInvalid() {
        HomologationPolicyRequestDTO dto = new HomologationPolicyRequestDTO(
                749, 31, "0000490", 0, null, null
        );

        Validator validator = Validation.buildDefaultValidatorFactory().getValidator();
        Set<ConstraintViolation<HomologationPolicyRequestDTO>> violations = validator.validate(dto);

        assertEquals(2, violations.size());
        assertTrue(violations.stream()
                .anyMatch(violation -> violation.getPropertyPath().toString().equals("startDate")));
        assertTrue(violations.stream()
                .anyMatch(violation -> violation.getPropertyPath().toString().equals("endDate")));
    }

    /* ------------------------------------------------------------------ */
    @Test
    @DisplayName("HomologationPolicyResponseDTO - builder sets all fields")
    void responseDTO_builderSetsAllFields() {
        HomologationPolicyResponseDTO dto = HomologationPolicyResponseDTO.builder()
                .id(1)
                .productCode(749)
                .branchCode(31)
                .policyNumber("0000490")
                .appliesValidity(0)
                .startDate(FECHA_INICIO)
                .endDate(FECHA_FIN)
                .build();

        assertAll(
                () -> assertEquals(1, dto.getId()),
                () -> assertEquals(749, dto.getProductCode()),
                () -> assertEquals(31, dto.getBranchCode()),
                () -> assertEquals("0000490", dto.getPolicyNumber()),
                () -> assertEquals(0, dto.getAppliesValidity()),
                () -> assertEquals(FECHA_INICIO, dto.getStartDate()),
                () -> assertEquals(FECHA_FIN, dto.getEndDate())
        );
    }

    @Test
    @DisplayName("HomologationPolicyResponseDTO - constructor without args and setters")
    void responseDTO_noArgsAndSetters() {
        HomologationPolicyResponseDTO dto = new HomologationPolicyResponseDTO();
        dto.setId(2);
        dto.setProductCode(1001);
        dto.setBranchCode(24);
        dto.setPolicyNumber("0000001");
        dto.setAppliesValidity(1);
        dto.setStartDate(FECHA_INICIO);
        dto.setEndDate(FECHA_FIN);

        assertAll(
                () -> assertEquals(2, dto.getId()),
                () -> assertEquals(1001, dto.getProductCode()),
                () -> assertEquals(24, dto.getBranchCode()),
                () -> assertEquals("0000001", dto.getPolicyNumber()),
                () -> assertEquals(1, dto.getAppliesValidity()),
                () -> assertEquals(FECHA_INICIO, dto.getStartDate()),
                () -> assertEquals(FECHA_FIN, dto.getEndDate())
        );
    }

    @Test
    @DisplayName("HomologationPolicyResponseDTO - builder creates non-null instance")
    void responseDTO_builderNotNull() {
        HomologationPolicyResponseDTO dto = HomologationPolicyResponseDTO.builder().build();
        assertNotNull(dto);
    }

    @Test
    @DisplayName("HomologationPolicyResponseDTO - optional fields can be null")
    void responseDTO_nullOptionalFields() {
        HomologationPolicyResponseDTO dto = HomologationPolicyResponseDTO.builder()
                .id(1)
                .productCode(749)
                .build();

        assertNull(dto.getStartDate());
        assertNull(dto.getEndDate());
        assertNull(dto.getAppliesValidity());
    }
}
