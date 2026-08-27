package co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Linea del XML contable devuelta por los procedimientos de Colombia.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ColombiaAccountingLine {

    private String family;
    private String period;
    private Integer pass;
    private String movementType;
    private String fileName;
    private Long sequence;
    private String content;
}


package co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia;

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
public class ColombiaXmlFile {

    private String family;
    private String period;
    private String movementType;
    private String fileName;
    private int lineCount;
    private String content;
}



package co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Archivo XML persistido expuesto por la API.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ColombiaXmlFileDTO {

    private Integer id;
    private String period;
    private String family;
    private String movementType;
    private String fileName;
    private Integer lineCount;
    private String processDate;
    private String status;
}



package co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

/**
 * Resultado de la generacion de asientos contables de Colombia.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ColombiaAccountingResultDTO {

    private String message;
    private String period;
    private List<ColombiaXmlFileDTO> files;
}
