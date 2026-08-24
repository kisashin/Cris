package co.com.bnpparibas.cardif.closingclaims.domain.dtos.cardifcenterclosing;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Archivo XML contable disponible para descarga.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AccountingXmlFileDTO {

    private Integer id;
    private String period;
    private String movementType;
    private String fileName;
    private Integer lineCount;
    private String processDate;
    private String status;
}
