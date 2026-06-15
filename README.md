PeruAccountingReportTest

package co.com.bnpparibas.cardif.closingclaims.domain.entity;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.time.LocalDateTime;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;

class PeruAccountingReportTest {

    @Test
    @DisplayName("Should create Peru accounting report using builder")
    void shouldCreatePeruAccountingReportUsingBuilder() {
        LocalDateTime movementDate =
                LocalDateTime.of(2026, 6, 15, 10, 30);

        LocalDateTime reportDate =
                LocalDateTime.of(2026, 6, 15, 11, 0);

        PeruAccountingReportId id =
                PeruAccountingReportId.builder()
                        .claimNumber("SIN-001")
                        .movementDate(movementDate)
                        .build();

        PeruAccountingReport report =
                PeruAccountingReport.builder()
                        .id(id)
                        .noticeDate("15/06/2026")
                        .product("Product test")
                        .productCode(123.0)
                        .certificate("CERT-001")
                        .initialReserve(1000.0)
                        .actualPayment(500.0)
                        .reserveBalance(500.0)
                        .reportDate(reportDate)
                        .scoringObjectionReason("Test reason")
                        .build();

        assertNotNull(report);
        assertEquals(id, report.getId());
        assertEquals("15/06/2026", report.getNoticeDate());
        assertEquals("Product test", report.getProduct());
        assertEquals(123.0, report.getProductCode());
        assertEquals("CERT-001", report.getCertificate());
        assertEquals(1000.0, report.getInitialReserve());
        assertEquals(500.0, report.getActualPayment());
        assertEquals(500.0, report.getReserveBalance());
        assertEquals(reportDate, report.getReportDate());
        assertEquals(
                "Test reason",
                report.getScoringObjectionReason());
    }

    @Test
    @DisplayName("Should create and update Peru accounting report")
    void shouldCreateAndUpdatePeruAccountingReport() {
        PeruAccountingReport report =
                new PeruAccountingReport();

        PeruAccountingReportId id =
                new PeruAccountingReportId(
                        "SIN-002",
                        LocalDateTime.of(2026, 6, 15, 12, 0));

        report.setId(id);
        report.setPartner("Partner test");
        report.setCurrency("PEN");
        report.setClaimStatus("APPROVED");
        report.setEmail("test@example.com");

        assertEquals(id, report.getId());
        assertEquals("Partner test", report.getPartner());
        assertEquals("PEN", report.getCurrency());
        assertEquals("APPROVED", report.getClaimStatus());
        assertEquals("test@example.com", report.getEmail());
    }
}
