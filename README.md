package co.com.bnpparibas.cardif.closingclaims.infraestructure.repository;

import org.hibernate.Session;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;
import java.sql.CallableStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

/**
 * Ejecuta procedimientos almacenados con timeout y cierre garantizado de
 * statements y cursores. Disponible para cualquier modulo del servicio.
 */
@Component
public class StoredProcedureExecutor {

    @PersistenceContext
    private EntityManager entityManager;

    @Value("${closing.stored-procedure.timeout-seconds:180}")
    private int timeoutSeconds;

    /**
     * Ejecuta un procedimiento y mapea todas las filas que devuelva.
     *
     * @param call sentencia de invocacion del procedimiento.
     * @param mapper mapeo de cada fila del resultado.
     * @param <T> tipo devuelto por el mapeo.
     * @return filas mapeadas; lista vacia si el procedimiento no devuelve datos.
     */
    public <T> List<T> query(
            String call,
            StoredProcedureRowMapper<T> mapper) {

        return entityManager.unwrap(Session.class)
                .doReturningWork(connection -> {
                    List<T> rows = new ArrayList<>();

                    try (CallableStatement statement =
                                 connection.prepareCall(call)) {

                        statement.setQueryTimeout(timeoutSeconds);
                        boolean hasResultSet = statement.execute();

                        while (hasResultSet
                                || statement.getUpdateCount() != -1) {

                            if (hasResultSet) {
                                readResultSet(statement, mapper, rows);
                            }

                            hasResultSet = statement.getMoreResults();
                        }
                    }

                    return rows;
                });
    }

    /**
     * Ejecuta un procedimiento y descarta cualquier resultado que devuelva.
     *
     * @param call sentencia de invocacion del procedimiento.
     */
    public void execute(String call) {
        entityManager.unwrap(Session.class).doWork(connection -> {
            try (CallableStatement statement =
                         connection.prepareCall(call)) {

                statement.setQueryTimeout(timeoutSeconds);
                boolean hasResultSet = statement.execute();

                while (hasResultSet || statement.getUpdateCount() != -1) {
                    if (hasResultSet) {
                        statement.getResultSet().close();
                    }
                    hasResultSet = statement.getMoreResults();
                }
            }
        });
    }

    private <T> void readResultSet(
            CallableStatement statement,
            StoredProcedureRowMapper<T> mapper,
            List<T> rows) throws SQLException {

        try (ResultSet resultSet = statement.getResultSet()) {
            while (resultSet.next()) {
                rows.add(mapper.map(resultSet));
            }
        }
    }

    public void setTimeoutSeconds(int timeoutSeconds) {
        this.timeoutSeconds = timeoutSeconds;
    }
}

package co.com.bnpparibas.cardif.closingclaims.infraestructure.repository;

import java.sql.ResultSet;
import java.sql.SQLException;

/**
 * Convierte una fila de un ResultSet en un objeto de dominio.
 *
 * @param <T> tipo devuelto por el mapeo.
 */
@FunctionalInterface
public interface StoredProcedureRowMapper<T> {

    /**
     * Mapea la fila actual del ResultSet.
     *
     * @param resultSet cursor posicionado en la fila a mapear.
     * @return objeto construido a partir de la fila.
     * @throws SQLException si falla la lectura de una columna.
     */
    T map(ResultSet resultSet) throws SQLException;
}

