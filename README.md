package co.com.bnpparibas.cardif.closingclaims.domain.dtos.homologation;

import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import javax.validation.constraints.Max;
import javax.validation.constraints.Min;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Positive;
import javax.validation.constraints.Size;
import java.time.LocalDate;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class HomologationPolicyRequestDTO {

    @NotNull(message = "Product code is required")
    @Positive(message = "Product code must be greater than zero")
    private Integer productCode;

    @NotNull(message = "Branch code is required")
    @Positive(message = "Branch code must be greater than zero")
    private Integer branchCode;

    @NotBlank(message = "Policy number is required")
    @Size(max = 50, message = "Policy number must not exceed 50 characters")
    private String policyNumber;

    @NotNull(message = "Applies validity is required")
    @Min(value = 0, message = "Applies validity must be 0 or 1")
    @Max(value = 1, message = "Applies validity must be 0 or 1")
    private Integer appliesValidity;

    @NotNull(message = "Start date is required")
    @JsonFormat(pattern = "yyyy-MM-dd")
    private LocalDate startDate;

    @NotNull(message = "End date is required")
    @JsonFormat(pattern = "yyyy-MM-dd")
    private LocalDate endDate;
}
