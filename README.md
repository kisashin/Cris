import java.sql.PreparedStatement;

import co.com.bnpparibas.cardif.cierres.domain.util.helpers.ClaimFileHelper;
    
    
    
    private static final String SQL_PATTERN =
            "SELECT patron FROM patronxprod_siniestros WHERE producto = :product";
    private static final String SQL_CLEAR_TEMP =
            "DELETE FROM tmpCargaSiniestrosAlfa";




    @Override
    public String findPattern(String product) {
        List<?> rows = entityManager.createNativeQuery(SQL_PATTERN)
                .setParameter("product", product)
                .getResultList();

        return rows.isEmpty() ? null : str(rows.get(0));
    }

    @Override
    public void clearTempClaims() {
        entityManager.createNativeQuery(SQL_CLEAR_TEMP).executeUpdate();
    }

    @Override
    public void insertTempClaims(List<String[]> rows) {
        entityManager.unwrap(Session.class).doWork(connection -> {

            try (PreparedStatement statement = connection.prepareStatement(SQL_INSERT_TEMP)) {

                int batch = 0;

                for (String[] row : rows) {
                    for (int i = 0; i < ClaimFileHelper.COLUMNS; i++) {
                        statement.setString(i + 1, row[i]);
                    }

                    statement.addBatch();
                    batch++;

                    if (batch % BATCH_SIZE == 0) {
                        statement.executeBatch();
                    }
                }

                statement.executeBatch();
            }
        });
    }

    @Override
    public String loadClaims(String product, String fileName) {
        try {
            List<Object[]> rows = callProcedure(SP_CARGA_ALFA, Integer.valueOf(product), fileName);

            return rows.isEmpty() ? "" : str(rows.get(0)[0]);
        } catch (Exception e) {
            log.error("Error ejecutando la carga de siniestros del producto {}", product, e);
            throw new DatabaseException(ExceptionConstants.DATABASE_CONNECTION, e);
        }
    }


    private static final int BATCH_SIZE = 100;
    private static final String SQL_INSERT_TEMP = buildTempInsert();




    private static String buildTempInsert() {
        StringBuilder placeholders = new StringBuilder();

        for (int i = 0; i < ClaimFileHelper.COLUMNS; i++) {
            placeholders.append(i == 0 ? "?" : ",?");
        }

        return "INSERT INTO tmpCargaSiniestrosAlfa VALUES (" + placeholders + ")";
    }



grep -rn "countProductLayout\|SP_CARGA\b" src --include=*.java    
