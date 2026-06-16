@Test
@DisplayName("Should generate Excel with headers and report data")
void shouldGenerateExcelWithHeadersAndReportData() throws IOException {

    System.out.println("=== INICIO TEST ===");
    System.out.println("java.io.tmpdir: " + System.getProperty("java.io.tmpdir"));

    LocalDateTime movementDate = LocalDateTime.of(2026, 6, 15, 10, 30);
    LocalDateTime reportDate = LocalDateTime.of(2026, 6, 15, 11, 0);

    System.out.println("=== CONSTRUYENDO REPORT ===");
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

    System.out.println("=== REPORT CONSTRUIDO: " + report + " ===");
    System.out.println("=== LLAMANDO generateExcel ===");

    byte[] file = helper.generateExcel(Collections.singletonList(report));

    System.out.println("=== generateExcel COMPLETADO, bytes: " + (file != null ? file.length : "NULL") + " ===");

    assertNotNull(file);
    assertTrue(file.length > 0);
    // ... resto igual
}
