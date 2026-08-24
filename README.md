            assertTrue(files.get(0).getProcessDate()
                    .startsWith("24/08/2026 03:03:29"));



    private static final DateTimeFormatter PROCESS_DATE_FORMAT =
            DateTimeFormatter.ofPattern(
                    "dd/MM/yyyy hh:mm:ss a", new Locale("es", "CO"));
