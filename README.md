ExcelFileResponseDto

package co.com.bnpparibas.cardif.cierres.domain.dtos;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class ExcelFileResponseDto {

    private String fileName;
    private String fileBase64;
}
