    @Test
    void countIncomplete_cuentaLasFilasConMenosColumnas() {
        String content = ClaimAccountingBuilder.csvRow("022") + "\n"
                + ClaimAccountingBuilder.csvRow("023", 10) + "\n"
                + ClaimAccountingBuilder.csvRow("024", 30);

        List<String[]> rows = helper.read(ClaimAccountingBuilder.csvFile(content));

        assertEquals(2, helper.countIncomplete(rows));
    }

    @Test
    void countIncomplete_conTodasLasColumnasDevuelveCero() {
        String content = ClaimAccountingBuilder.csvRow("022") + "\n"
                + ClaimAccountingBuilder.csvRow("023");

        List<String[]> rows = helper.read(ClaimAccountingBuilder.csvFile(content));

        assertEquals(0, helper.countIncomplete(rows));
    }

    @Test
    void countIncomplete_conCamposVaciosAlFinalNoCuentaComoIncompleta() {
        String content = ClaimAccountingBuilder.csvRow("022", 43) + ";;;";

        List<String[]> rows = helper.read(ClaimAccountingBuilder.csvFile(content));

        assertEquals(0, helper.countIncomplete(rows));
    }
