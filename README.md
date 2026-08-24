package co.com.bnpparibas.cardif.closingclaims.domain.dtos.cardifcenterclosing;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

/**
 * Resultado de la generacion de asientos contables de Centroamerica.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CenterAccountingResultDTO {

    private String message;
    private String period;
    private List<AccountingXmlFileDTO> files;
}
