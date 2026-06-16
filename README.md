
PeruAccountingReportIdTest

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

@Test
@DisplayName("Should cover equals and hashCode branches")
void shouldCoverEqualsAndHashCodeBranches() {
    LocalDateTime movementDate =
            LocalDateTime.of(2026, 6, 15, 12, 0);

    LocalDateTime differentMovementDate =
            LocalDateTime.of(2026, 6, 16, 12, 0);

    PeruAccountingReportId base =
            new PeruAccountingReportId(
                    "SIN-001",
                    movementDate);

    PeruAccountingReportId equal =
            new PeruAccountingReportId(
                    "SIN-001",
                    movementDate);

    PeruAccountingReportId differentClaim =
            new PeruAccountingReportId(
                    "SIN-002",
                    movementDate);

    PeruAccountingReportId differentMovement =
            new PeruAccountingReportId(
                    "SIN-001",
                    differentMovementDate);

    PeruAccountingReportId nullClaim =
            new PeruAccountingReportId(
                    null,
                    movementDate);

    PeruAccountingReportId nullMovement =
            new PeruAccountingReportId(
                    "SIN-001",
                    null);

    PeruAccountingReportId allNull =
            new PeruAccountingReportId(
                    null,
                    null);

    PeruAccountingReportId anotherAllNull =
            new PeruAccountingReportId(
                    null,
                    null);

    assertTrue(base.equals(base));
    assertTrue(base.equals(equal));
    assertFalse(base.equals(null));
    assertFalse(base.equals("invalid-type"));
    assertFalse(base.equals(differentClaim));
    assertFalse(base.equals(differentMovement));

    assertFalse(base.equals(nullClaim));
    assertFalse(nullClaim.equals(base));

    assertFalse(base.equals(nullMovement));
    assertFalse(nullMovement.equals(base));

    assertTrue(allNull.equals(anotherAllNull));

    assertEquals(base.hashCode(), equal.hashCode());
    assertEquals(allNull.hashCode(), anotherAllNull.hashCode());
}


PeruAccountingReportTest.java

import java.lang.reflect.Method;

import static org.junit.jupiter.api.Assertions.assertTrue;

@Test
@DisplayName("Should cover all entity setters and getters")
void shouldCoverAllEntitySettersAndGetters()
        throws ReflectiveOperationException {

    PeruAccountingReport report = new PeruAccountingReport();
    int testedSetters = 0;

    for (Method setter : PeruAccountingReport.class.getMethods()) {
        if (isSetter(setter)) {
            Object expectedValue =
                    createTestValue(setter.getParameterTypes()[0]);

            setter.invoke(report, expectedValue);

            String getterName =
                    "get" + setter.getName().substring(3);

            Method getter =
                    PeruAccountingReport.class.getMethod(getterName);

            assertEquals(
                    expectedValue,
                    getter.invoke(report),
                    setter.getName());

            testedSetters++;
        }
    }

    assertTrue(testedSetters > 100);
}
