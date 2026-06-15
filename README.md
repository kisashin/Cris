src/test/java/co/com/bnpparibas/cardif/closingclaims/domain/util/helpers/PeruAccountingReportMapperTest.java

package co.com.bnpparibas.cardif.closingclaims.domain.util.helpers;

import co.com.bnpparibas.cardif.closingclaims.domain.dtos.peruaccountingreport.PeruAccountingReportResponseDTO;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.mapstruct.factory.Mappers;

import java.time.LocalDateTime;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;

class PeruAccountingReportMapperTest {

    private final PeruAccountingReportMapper mapper =
            Mappers.getMapper(PeruAccountingReportMapper.class);

    @Test
    @DisplayName("Should map report date to response DTO")
    void shouldMapReportDateToResponseDTO() {
        LocalDateTime reportDate =
                LocalDateTime.of(2026, 6, 15, 10, 30);

        PeruAccountingReportResponseDTO result =
                mapper.toResponseDTO(reportDate);

        assertNotNull(result);
        assertEquals(reportDate, result.getReportDate());
    }

    @Test
    @DisplayName("Should create response DTO with null report date")
    void shouldCreateResponseDTOWithNullReportDate() {
        PeruAccountingReportResponseDTO result =
                mapper.toResponseDTO(null);

        assertNotNull(result);
        assertEquals(null, result.getReportDate());
    }
}
