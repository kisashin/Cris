package co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Estado del reporte mensual de Aval expuesto por la API.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AvalReportFileDTO {

    private Integer id;
    private String period;
    private String fileName;
    private Integer rowCount;
    private String processDate;
    private String status;
    private int pendingMovements;
}
