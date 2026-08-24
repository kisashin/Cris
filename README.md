package co.com.bnpparibas.cardif.closingclaims.domain.dtos.cardifcenterclosing;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Linea del XML contable devuelta por el procedimiento de contabilizacion.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AccountingXmlLine {

    private String period;
    private Integer pass;
    private Integer lineType;
    private String movementType;
    private Long sequence;
    private String content;
}





package co.com.bnpparibas.cardif.closingclaims.domain.dtos.cardifcenterclosing;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Archivo XML generado para un tipo de movimiento, con su contenido en Base64.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AccountingXmlFileDTO {

    private String movementType;
    private String fileName;
    private int lineCount;
    private String content;
}



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
    private String processDate;
    private String status;
    private String period;
    private List<AccountingXmlFileDTO> files;
}



