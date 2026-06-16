private void closeWorkbook(SXSSFWorkbook workbook)
        throws IOException {

    if (workbook == null) {
        return;
    }

    try {
        workbook.dispose();
    } finally {
        workbook.close();
    }
}
