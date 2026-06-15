src/test/java/co/com/bnpparibas/cardif/closingclaims/domain/entity/PeruAccountingReportIdTest.java

package co.com.bnpparibas.cardif.closingclaims.domain.entity;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.time.LocalDateTime;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;

class PeruAccountingReportIdTest {

    @Test
    @DisplayName("Should create composite identifier using builder")
    void shouldCreateCompositeIdentifierUsingBuilder() {
        LocalDateTime movementDate =
                LocalDateTime.of(2026, 6, 15, 10, 30);

        PeruAccountingReportId id =
                PeruAccountingReportId.builder()
                        .claimNumber("SIN-001")
                        .movementDate(movementDate)
                        .build();

        assertNotNull(id);
        assertEquals("SIN-001", id.getClaimNumber());
        assertEquals(movementDate, id.getMovementDate());
    }

    @Test
    @DisplayName("Should create and update composite identifier")
    void shouldCreateAndUpdateCompositeIdentifier() {
        PeruAccountingReportId id =
                new PeruAccountingReportId();

        LocalDateTime movementDate =
                LocalDateTime.of(2026, 6, 15, 11, 0);

        id.setClaimNumber("SIN-002");
        id.setMovementDate(movementDate);

        assertEquals("SIN-002", id.getClaimNumber());
        assertEquals(movementDate, id.getMovementDate());
    }

    @Test
    @DisplayName("Should compare composite identifiers correctly")
    void shouldCompareCompositeIdentifiersCorrectly() {
        LocalDateTime movementDate =
                LocalDateTime.of(2026, 6, 15, 12, 0);

        PeruAccountingReportId firstId =
                new PeruAccountingReportId(
                        "SIN-003",
                        movementDate);

        PeruAccountingReportId secondId =
                new PeruAccountingReportId(
                        "SIN-003",
                        movementDate);

        PeruAccountingReportId differentId =
                new PeruAccountingReportId(
                        "SIN-004",
                        movementDate);

        assertEquals(firstId, secondId);
        assertEquals(firstId.hashCode(), secondId.hashCode());
        assertNotEquals(firstId, differentId);
    }
}
