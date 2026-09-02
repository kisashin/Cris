    private static final DateTimeFormatter DATE_FORMATTER =
            DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm:ss", new Locale("es", "CO"));


    @Override
    public List<AccountingFileDto> findFiles(String period) {
        List<Object[]> rows = entityManager.createNativeQuery(SQL_FILES)
                .setParameter("period", period)
                .getResultList();

        return rows.stream()
                .map(row -> new AccountingFileDto(
                        ((Number) row[0]).intValue(),
                        str(row[1]),
                        str(row[2]),
                        str(row[3]),
                        formatDate(row[4])))
                .collect(Collectors.toList());
    }


    private static String formatDate(Object value) {
        if (value == null) {
            return null;
        }

        return ((Timestamp) value).toLocalDateTime().format(DATE_FORMATTER);
    }


import java.sql.Timestamp;
import java.time.format.DateTimeFormatter;
import java.util.Locale;    
