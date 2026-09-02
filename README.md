import java.util.Date;

import co.com.bnpparibas.cardif.cierres.domain.dtos.AccountingFileDto;
import co.com.bnpparibas.cardif.cierres.domain.dtos.DownloadFileDto;
import co.com.bnpparibas.cardif.cierres.domain.dtos.XmlFileDto;
    
    
    private static final String SQL_DELETE_FILES =
            "DELETE FROM archivoAsientoReaseguro WHERE producto = :product AND periodoContable = :period";
    private static final String SQL_INSERT_FILE =
            "INSERT INTO archivoAsientoReaseguro "
            + "(producto, tipoDiario, periodoContable, nombreArchivo, contenido, fechaGeneracion, usuario) "
            + "VALUES (:product, :journalType, :period, :fileName, :content, GETDATE(), :user)";
    private static final String SQL_FILES =
            "SELECT id, producto, tipoDiario, nombreArchivo, fechaGeneracion "
            + "FROM archivoAsientoReaseguro WHERE periodoContable = :period "
            + "ORDER BY producto, tipoDiario";
    private static final String SQL_FILE =
            "SELECT nombreArchivo, contenido FROM archivoAsientoReaseguro WHERE id = :id";



    private static final String SCREEN_DESTINATION = "PANTALLA";



        @Override
    public XmlFileDto generateXml(String journalType, String period, String product, String comment) {
        try {
            List<Object[]> rows = callProcedure(SP_XML, journalType, period, product, comment, SCREEN_DESTINATION);

            if (rows.isEmpty()) {
                return null;
            }

            Object[] row = rows.get(0);
            String content = str(row[2]);

            if (content == null || content.isEmpty() || NO_XML.equals(content)) {
                return null;
            }

            return new XmlFileDto(str(row[0]), str(row[1]), content);
        } catch (Exception e) {
            log.error("Error generando el XML {} del producto {}", journalType, product, e);
            throw new DatabaseException(ExceptionConstants.DATABASE_CONNECTION, e);
        }
    }


        @Override
    public void deleteFiles(String product, String period) {
        entityManager.createNativeQuery(SQL_DELETE_FILES)
                .setParameter("product", product)
                .setParameter("period", period)
                .executeUpdate();
    }

    @Override
    public void saveFile(String product, String journalType, String period,
                         String fileName, String content, String user) {
        entityManager.createNativeQuery(SQL_INSERT_FILE)
                .setParameter("product", product)
                .setParameter("journalType", journalType)
                .setParameter("period", period)
                .setParameter("fileName", fileName)
                .setParameter("content", content)
                .setParameter("user", user)
                .executeUpdate();
    }

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
                        (Date) row[4]))
                .collect(Collectors.toList());
    }

    @Override
    public DownloadFileDto findFile(Integer id) {
        List<Object[]> rows = entityManager.createNativeQuery(SQL_FILE)
                .setParameter("id", id)
                .getResultList();

        if (rows.isEmpty()) {
            return null;
        }

        return new DownloadFileDto(str(rows.get(0)[0]), str(rows.get(0)[1]));
    }
