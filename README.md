package co.com.bnpparibas.cardif.closingclaims.domain.dtos.individualnews;

import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ClaimMovementResponseDTO {

    private Long idCarvajal;
    private String claimNumber;
    private String identificationNumber;
    private String productCode;
    private String planCode;
    private String coverage;
    private String branchCode;
    private BigDecimal movementValue;

    @JsonFormat(pattern = "yyyy-MM-dd")
    private LocalDateTime movementDate;

    private String movementType;
    private String partner;
    private String cardifId;
    private String claimKey;
    private Integer partnerCode;
    private String claimStatus;
    private String majorStatus;
    private String channel;
    private String pandemic;
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