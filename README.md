src/test/java/co/com/bnpparibas/cardif/closingclaims/domain/dtos/peruaccountingreport/PeruAccountingReportResponseDTOTest.java

package co.com.bnpparibas.cardif.closingclaims.domain.dtos.peruaccountingreport;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.time.LocalDateTime;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;

class PeruAccountingReportResponseDTOTest {

    @Test
    @DisplayName("Should create response DTO using builder")
    void shouldCreateResponseDTOUsingBuilder() {
        LocalDateTime reportDate =
                LocalDateTime.of(2026, 6, 15, 10, 30);

        PeruAccountingReportResponseDTO response =
                PeruAccountingReportResponseDTO.builder()
                        .reportDate(reportDate)
                        .build();

        assertNotNull(response);
        assertEquals(reportDate, response.getReportDate());
    }

    @Test
    @DisplayName("Should create and update response DTO")
    void shouldCreateAndUpdateResponseDTO() {
        PeruAccountingReportResponseDTO response =
                new PeruAccountingReportResponseDTO();

        LocalDateTime reportDate =
                LocalDateTime.of(2026, 6, 15, 11, 0);

        response.setReportDate(reportDate);

        assertEquals(reportDate, response.getReportDate());
    }

    @Test
    @DisplayName("Should create response DTO using all arguments constructor")
    void shouldCreateResponseDTOUsingAllArgumentsConstructor() {
        LocalDateTime reportDate =
                LocalDateTime.of(2026, 6, 15, 12, 0);

        PeruAccountingReportResponseDTO response =
                new PeruAccountingReportResponseDTO(reportDate);

        assertEquals(reportDate, response.getReportDate());
    }
}
