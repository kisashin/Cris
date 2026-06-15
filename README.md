PeruAccountingReportResponseDTO

package co.com.bnpparibas.cardif.closingclaims.domain.dtos.peruaccountingreport;

import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.io.Serializable;
import java.time.LocalDateTime;

/**
 * Respuesta con la información de generación del reporte contable de Perú.
 */
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class PeruAccountingReportResponseDTO implements Serializable {

    private static final long serialVersionUID = 1L;

    /**
     * Fecha de la última generación del reporte.
     */
    @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss")
    private LocalDateTime reportDate;
}

src/main/java/co/com/bnpparibas/cardif/closingclaims/domain/util/helpers/PeruAccountingReportMapper.java

package co.com.bnpparibas.cardif.closingclaims.domain.util.helpers;

import co.com.bnpparibas.cardif.closingclaims.domain.dtos.peruaccountingreport.PeruAccountingReportResponseDTO;
import org.mapstruct.Mapper;

import java.time.LocalDateTime;

/**
 * Mapper para las respuestas del reporte contable de Perú.
 */
@Mapper(componentModel = "spring")
public interface PeruAccountingReportMapper {

    /**
     * Convierte la fecha de generación en el DTO de respuesta.
     *
     * @param reportDate fecha de la última generación.
     * @return DTO con la fecha del reporte.
     */
    default PeruAccountingReportResponseDTO toResponseDTO(LocalDateTime reportDate) {
        return PeruAccountingReportResponseDTO.builder()
                .reportDate(reportDate)
                .build();
    }
}
