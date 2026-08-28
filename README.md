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
public class AvalReportStatusDTO {

    private String generationDate;
    private int pendingMovements;
}


package co.com.bnpparibas.cardif.closingclaims.infraestructure.repository;

import co.com.bnpparibas.cardif.closingclaims.domain.entity.TmpRepAvalCierre;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

@Repository
public interface AvalReportRepository
        extends JpaRepository<TmpRepAvalCierre, Long> {

    @Query(
            value = "SELECT COUNT(*) FROM historicomovimientos "
                    + "WHERE Fechacontabilizacion IS NULL "
                    + "AND marcaavalpos IS NULL "
                    + "AND socio IN ('BANCO DE BOGOTA','BANCO AV VILLAS',"
                    + "'BANCO DE OCCIDENTE','BANCO POPULAR') "
                    + "AND CodProducto NOT IN "
                    + "(SELECT producto FROM dbo.productosnoaval)",
            nativeQuery = true)
    int countPendingMovements();
}
