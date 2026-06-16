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

private boolean isSetter(Method method) {
    return method.getName().startsWith("set")
            && method.getParameterCount() == 1
            && method.getReturnType().equals(void.class);
}

private Object createTestValue(Class<?> fieldType) {
    if (String.class.equals(fieldType)) {
        return "test-value";
    }

    if (Double.class.equals(fieldType)) {
        return 100.0D;
    }

    if (LocalDateTime.class.equals(fieldType)) {
        return LocalDateTime.of(2026, 6, 15, 10, 30);
    }

    if (PeruAccountingReportId.class.equals(fieldType)) {
        return new PeruAccountingReportId(
                "SIN-001",
                LocalDateTime.of(2026, 6, 15, 10, 30));
    }

    throw new IllegalArgumentException(
            "Unsupported field type: " + fieldType.getName());
}
