package co.com.bnpparibas.cardif.closingclaims.domain.dtos.individualnews;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class IndividualNewsDeleteRequestDTO {

    @NotNull(message = "Carvajal identifier is required")
    private Long idCarvajal;

    @NotBlank(message = "Justification is required")
    @Size(max = 255, message = "Justification must not exceed 255 characters")
    private String justification;
}