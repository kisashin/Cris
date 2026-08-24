package co.com.bnpparibas.cardif.closingclaims.domain.dtos.cardifcenterclosing;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Archivo XML armado en memoria antes de persistirse.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AccountingXmlFile {

    private String movementType;
    private String fileName;
    private int lineCount;
    private String content;
}
