package co.com.bnpparibas.cardif.closingclaims.domain.dtos.individualnews;

import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;
import java.time.LocalDateTime;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class IndividualNewsRequestDTO {

    @NotNull(message = "Carvajal identifier is required")
    private Long idCarvajal;

    @NotBlank(message = "Movement type is required")
    @Size(max = 100, message = "Movement type must not exceed 100 characters")
    private String movementType;

    @NotBlank(message = "Partner is required")
    @Size(max = 255, message = "Partner must not exceed 255 characters")
    private String partner;

    @NotBlank(message = "Coverage is required")
    @Size(max = 255, message = "Coverage must not exceed 255 characters")
    private String coverage;

    @NotBlank(message = "Cardif identifier is required")
    @Size(max = 255, message = "Cardif identifier must not exceed 255 characters")
    private String cardifId;

    @NotBlank(message = "Claim key is required")
    @Size(max = 255, message = "Claim key must not exceed 255 characters")
    private String claimKey;

    @NotBlank(message = "Branch code is required")
    @Size(max = 120, message = "Branch code must not exceed 120 characters")
    private String branchCode;

    @NotBlank(message = "Claim number is required")
    @Size(max = 255, message = "Claim number must not exceed 255 characters")
    private String claimNumber;

    @NotNull(message = "Partner code is required")
    private Integer partnerCode;

    @NotBlank(message = "Claim status is required")
    @Size(max = 100, message = "Claim status must not exceed 100 characters")
    private String claimStatus;

    @NotBlank(message = "Major status is required")
    @Size(max = 255, message = "Major status must not exceed 255 characters")
    private String majorStatus;

    @NotBlank(message = "Channel is required")
    @Size(max = 255, message = "Channel must not exceed 255 characters")
    private String channel;

    @NotBlank(message = "Pandemic is required")
    @Size(max = 255, message = "Pandemic must not exceed 255 characters")
    private String pandemic;

    @NotBlank(message = "Justification is required")
    @Size(max = 255, message = "Justification must not exceed 255 characters")
    private String justification;

    @Size(max = 255, message = "Payment beneficiary must not exceed 255 characters")
    private String paymentBeneficiary;

    private Integer coinsuranceType;

    private Double retainedCoinsuranceValue;

    private Double cededCoinsuranceValue;

    @JsonFormat(pattern = "yyyy-MM-dd")
    private LocalDateTime birthDate;

    @JsonFormat(pattern = "yyyy-MM-dd")
    private LocalDateTime occurrenceDate;

    @JsonFormat(pattern = "yyyy-MM-dd")
    private LocalDateTime partnerNoticeDate;

    @JsonFormat(pattern = "yyyy-MM-dd")
    private LocalDateTime cardifNoticeDate;
}