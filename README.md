GenerateAccountingRequestDto

package co.com.bnpparibas.cardif.cierres.api.dtos;

import javax.validation.constraints.NotBlank;

import co.com.bnpparibas.cardif.cierres.domain.util.constants.ExceptionConstants;
import lombok.Data;

@Data
public class GenerateAccountingRequestDto {

	@NotBlank(message = ExceptionConstants.REQUIRED_FIELD)
	private String product;

	@NotBlank(message = ExceptionConstants.REQUIRED_FIELD)
	private String comment;
}
