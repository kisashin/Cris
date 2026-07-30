ReportStoredProcedureRepository

package co.com.bnpparibas.cardif.closingclaims.infraestructure.repository;

import co.com.bnpparibas.cardif.closingclaims.domain.dtos.loaddata.ReportTabularDto;
import org.hibernate.Session;
import org.springframework.stereotype.Repository;

import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;
import java.sql.CallableStatement;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

/**
 * Ejecuta los procedimientos almacenados de reportes recuperando
 * los datos y los nombres de columna del result set.
 *
 * Los nombres se toman de ResultSetMetaData, que es el equivalente
 * al DataTable.Columns que usaba el GridView del legacy con
 * AutoGenerateColumns. No se quema ningun nombre de columna.
 */
@Repository
public class ReportStoredProcedureRepository {

    /** Longitud maxima de una celda de Excel. */
    private static final int EXCEL_MAX_CELL_LENGTH = 32767;

    @PersistenceContext
    private EntityManager entityManager;

    /**
     * @param storedProcedure nombre calificado del procedimiento,
     *                        por ejemplo dbo.SP_Reporte_Datos_Siniestros
     * @return cabeceras y filas del primer result set del procedimiento.
     */
    public ReportTabularDto execute(final String storedProcedure) {
        Session session = entityManager.unwrap(Session.class);
        return session.doReturningWork(connection ->
                readFirstResultSet(connection, storedProcedure));
    }

    /**
     * Visibilidad de paquete para permitir pruebas unitarias con
     * mocks de java.sql, sin base de datos ni archivos temporales.
     */
    ReportTabularDto readFirstResultSet(final Connection connection,
                                        final String storedProcedure)
            throws SQLException {

        try (CallableStatement statement =
                     connection.prepareCall("{call " + storedProcedure + "}")) {

            boolean hasResultSet = statement.execute();

            while (true) {
                if (hasResultSet) {
                    try (ResultSet resultSet = statement.getResultSet()) {
                        return map(resultSet);
                    }
                }
                if (statement.getUpdateCount() == -1) {
                    return ReportTabularDto.empty();
                }
                hasResultSet = statement.getMoreResults();
            }
        }
    }

    /** Visibilidad de paquete para permitir pruebas unitarias. */
    ReportTabularDto map(final ResultSet resultSet) throws SQLException {

        ResultSetMetaData metaData = resultSet.getMetaData();
        int columnCount = metaData.getColumnCount();

        List<String> headers = new ArrayList<>(columnCount);
        for (int index = 1; index <= columnCount; index++) {
            headers.add(metaData.getColumnLabel(index));
        }

        List<String[]> rows = new ArrayList<>();
        while (resultSet.next()) {
            String[] row = new String[columnCount];
            for (int index = 1; index <= columnCount; index++) {
                row[index - 1] = readAsText(resultSet, index);
            }
            rows.add(row);
        }

        return new ReportTabularDto(headers, rows);
    }

    /**
     * Todo se lee como texto para replicar el mso-number-format:@ del
     * legacy y evitar la corrupcion de identificadores largos como
     * Certificado. Los procedimientos ya devuelven fechas y valores
     * formateados con CONVERT(varchar, ..., 103) y replace('.', ',').
     */
    private String readAsText(final ResultSet resultSet, final int index)
            throws SQLException {

        String value = resultSet.getString(index);

        if (value == null) {
            return "";
        }
        if (value.length() > EXCEL_MAX_CELL_LENGTH) {
            return value.substring(0, EXCEL_MAX_CELL_LENGTH);
        }
        return value;
    }
}
