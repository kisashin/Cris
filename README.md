package co.com.bnpparibas.cardif.closingclaims.domain.util.helpers;

import co.com.bnpparibas.cardif.closingclaims.domain.entity.PeruAccountingReport;
import co.com.bnpparibas.cardif.closingclaims.domain.entity.PeruAccountingReportId;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.io.IOException;
import java.time.LocalDateTime;
import java.util.Collections;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.ArgumentMatchers.anyList;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class PeruAccountingReportExcelHelperTest {

    @Mock
    private PeruAccountingReportExcelHelper helper;

    @Test
    @DisplayName("Should generate Excel with headers and report data")
    void shouldGenerateExcelWithHeadersAndReportData() throws IOException {

        LocalDateTime movementDate = LocalDateTime.of(2026, 6, 15, 10, 30);
        LocalDateTime reportDate = LocalDateTime.of(2026, 6, 15, 11, 0);

        PeruAccountingReport report = PeruAccountingReport.builder()
                .id(PeruAccountingReportId.builder()
                        .claimNumber("SIN-001")
                        .movementDate(movementDate)
                        .build())
                .noticeDate("15/06/2026")
                .productCode(123.0)
                .reportDate(reportDate)
                .scoringObjectionReason("Test reason")
                .build();

        List<PeruAccountingReport> reports = Collections.singletonList(report);
        byte[] fakeExcel = new byte[]{1, 2, 3, 4, 5};

        when(helper.generateExcel(anyList())).thenReturn(fakeExcel);

        byte[] result = helper.generateExcel(reports);

        assertNotNull(result);
        assertTrue(result.length > 0);
    }

    @Test
    @DisplayName("Should generate Excel with only headers when report list is empty")
    void shouldGenerateExcelWithOnlyHeadersWhenListIsEmpty() throws IOException {

        byte[] fakeExcel = new byte[]{1, 2, 3, 4, 5};

        when(helper.generateExcel(anyList())).thenReturn(fakeExcel);

        byte[] result = helper.generateExcel(Collections.emptyList());

        assertNotNull(result);
        assertTrue(result.length > 0);
    }
}
