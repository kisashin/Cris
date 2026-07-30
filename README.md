ReportStoredProcedureRepositoryTest

package co.com.bnpparibas.cardif.closingclaims.infraestructure.repository;

import co.com.bnpparibas.cardif.closingclaims.domain.dtos.loaddata.ReportTabularDto;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import org.mockito.junit.jupiter.MockitoSettings;
import org.mockito.quality.Strictness;

import java.sql.CallableStatement;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.*;

/**
 * Pruebas de la lectura del result set. Se mockean las interfaces de
 * java.sql, por lo que no se requiere base de datos, archivos
 * temporales ni acceso a red.
 */
@ExtendWith(MockitoExtension.class)
@MockitoSettings(strictness = Strictness.LENIENT)
class ReportStoredProcedureRepositoryTest {

    private static final String SP = "dbo.SP_Reporte_Datos_Siniestros";

    private final ReportStoredProcedureRepository repository =
            new ReportStoredProcedureRepository();

    /** Arma un ResultSet mockeado con las cabeceras y filas indicadas. */
    private ResultSet mockResultSet(final String[] headers,
                                    final String[][] rows) throws SQLException {

        ResultSetMetaData metaData = mock(ResultSetMetaData.class);
        when(metaData.getColumnCount()).thenReturn(headers.length);

        for (int index = 0; index < headers.length; index++) {
            when(metaData.getColumnLabel(index + 1)).thenReturn(headers[index]);
        }

        ResultSet resultSet = mock(ResultSet.class);
        when(resultSet.getMetaData()).thenReturn(metaData);

        Boolean[] nextValues = new Boolean[rows.length + 1];
        for (int index = 0; index < rows.length; index++) {
            nextValues[index] = Boolean.TRUE;
        }
        nextValues[rows.length] = Boolean.FALSE;

        if (rows.length == 0) {
            when(resultSet.next()).thenReturn(false);
        } else {
            Boolean[] rest = new Boolean[nextValues.length - 1];
            System.arraycopy(nextValues, 1, rest, 0, rest.length);
            when(resultSet.next()).thenReturn(nextValues[0], rest);
        }

        for (int column = 0; column < headers.length; column++) {
            if (rows.length == 0) {
                continue;
            }
            String first = rows[0][column];
            String[] rest = new String[rows.length - 1];
            for (int row = 1; row < rows.length; row++) {
                rest[row - 1] = rows[row][column];
            }
            when(resultSet.getString(column + 1)).thenReturn(first, rest);
        }

        return resultSet;
    }

    // =========================
    // MAPEO DE CABECERAS Y DATOS
    // =========================

    @Test
    void map_shouldReadHeadersFromMetadata() throws SQLException {

        ResultSet resultSet = mockResultSet(
                new String[]{"Llavesiniestro", "Socio", "Edad"},
                new String[][]{{"SIN-1", "BANISTMO S.A", "43"}});

        ReportTabularDto result = repository.map(resultSet);

        assertTrue(result.hasColumns());
        assertEquals(3, result.getHeaders().size());
        assertEquals("Llavesiniestro", result.getHeaders().get(0));
        assertEquals("Socio", result.getHeaders().get(1));
        assertEquals("Edad", result.getHeaders().get(2));
    }

    @Test
    void map_shouldReadRows() throws SQLException {

        ResultSet resultSet = mockResultSet(
                new String[]{"Llavesiniestro", "Socio"},
                new String[][]{
                        {"SIN-1", "BANISTMO S.A"},
                        {"SIN-2", "BANISTMO S.A"}
                });

        ReportTabularDto result = repository.map(resultSet);

        assertEquals(2, result.getRows().size());
        assertEquals("SIN-1", result.getRows().get(0)[0]);
        assertEquals("SIN-2", result.getRows().get(1)[0]);
    }

    @Test
    void map_withHeadersAndNoRows() throws SQLException {

        ResultSet resultSet = mockResultSet(
                new String[]{"Llavesiniestro"},
                new String[][]{});

        ReportTabularDto result = repository.map(resultSet);

        assertTrue(result.hasColumns());
        assertTrue(result.getRows().isEmpty());
    }

    // =========================
    // LECTURA COMO TEXTO
    // =========================

    @Test
    void map_shouldConvertNullToEmptyString() throws SQLException {

        ResultSetMetaData metaData = mock(ResultSetMetaData.class);
        when(metaData.getColumnCount()).thenReturn(1);
        when(metaData.getColumnLabel(1)).thenReturn("Distrito");

        ResultSet resultSet = mock(ResultSet.class);
        when(resultSet.getMetaData()).thenReturn(metaData);
        when(resultSet.next()).thenReturn(true, false);
        when(resultSet.getString(1)).thenReturn(null);

        ReportTabularDto result = repository.map(resultSet);

        assertEquals("", result.getRows().get(0)[0]);
    }

    @Test
    void map_shouldTruncateValuesLongerThanExcelLimit() throws SQLException {

        StringBuilder builder = new StringBuilder();
        for (int index = 0; index < 40000; index++) {
            builder.append('A');
        }

        ResultSetMetaData metaData = mock(ResultSetMetaData.class);
        when(metaData.getColumnCount()).thenReturn(1);
        when(metaData.getColumnLabel(1)).thenReturn("Informacion");

        ResultSet resultSet = mock(ResultSet.class);
        when(resultSet.getMetaData()).thenReturn(metaData);
        when(resultSet.next()).thenReturn(true, false);
        when(resultSet.getString(1)).thenReturn(builder.toString());

        ReportTabularDto result = repository.map(resultSet);

        assertEquals(32767, result.getRows().get(0)[0].length());
    }

    @Test
    void map_shouldKeepValuesWithinExcelLimit() throws SQLException {

        ResultSet resultSet = mockResultSet(
                new String[]{"Certificado"},
                new String[][]{{"'8902875520925260"}});

        ReportTabularDto result = repository.map(resultSet);

        assertEquals("'8902875520925260", result.getRows().get(0)[0]);
    }

    // =========================
    // RECORRIDO DEL CALLABLE STATEMENT
    // =========================

    @Test
    void readFirstResultSet_shouldReturnFirstResultSet() throws SQLException {

        ResultSet resultSet = mockResultSet(
                new String[]{"Socio"},
                new String[][]{{"BANISTMO S.A"}});

        CallableStatement statement = mock(CallableStatement.class);
        when(statement.execute()).thenReturn(true);
        when(statement.getResultSet()).thenReturn(resultSet);

        Connection connection = mock(Connection.class);
        when(connection.prepareCall(anyString())).thenReturn(statement);

        ReportTabularDto result = repository.readFirstResultSet(connection, SP);

        assertTrue(result.hasColumns());
        assertEquals(1, result.getRows().size());
    }

    /** El procedimiento emite conteos intermedios antes del rowset real. */
    @Test
    void readFirstResultSet_shouldSkipIntermediateUpdateCounts() throws SQLException {

        ResultSet resultSet = mockResultSet(
                new String[]{"Socio"},
                new String[][]{{"BANISTMO S.A"}});

        CallableStatement statement = mock(CallableStatement.class);
        when(statement.execute()).thenReturn(false);
        when(statement.getUpdateCount()).thenReturn(5, 3);
        when(statement.getMoreResults()).thenReturn(false, true);
        when(statement.getResultSet()).thenReturn(resultSet);

        Connection connection = mock(Connection.class);
        when(connection.prepareCall(anyString())).thenReturn(statement);

        ReportTabularDto result = repository.readFirstResultSet(connection, SP);

        assertTrue(result.hasColumns());
    }

    /** El procedimiento no devuelve ningun result set. */
    @Test
    void readFirstResultSet_shouldReturnEmptyWhenNoResultSet() throws SQLException {

        CallableStatement statement = mock(CallableStatement.class);
        when(statement.execute()).thenReturn(false);
        when(statement.getUpdateCount()).thenReturn(-1);

        Connection connection = mock(Connection.class);
        when(connection.prepareCall(anyString())).thenReturn(statement);

        ReportTabularDto result = repository.readFirstResultSet(connection, SP);

        assertFalse(result.hasColumns());
        assertTrue(result.getRows().isEmpty());
    }

    @Test
    void readFirstResultSet_shouldBuildCallSyntax() throws SQLException {

        CallableStatement statement = mock(CallableStatement.class);
        when(statement.execute()).thenReturn(false);
        when(statement.getUpdateCount()).thenReturn(-1);

        Connection connection = mock(Connection.class);
        when(connection.prepareCall(anyString())).thenReturn(statement);

        repository.readFirstResultSet(connection, SP);

        verify(connection).prepareCall("{call " + SP + "}");
    }

    @Test
    void readFirstResultSet_shouldPropagateSqlException() throws SQLException {

        Connection connection = mock(Connection.class);
        when(connection.prepareCall(anyString()))
                .thenThrow(new SQLException("fallo de conexion"));

        assertThrows(SQLException.class,
                () -> repository.readFirstResultSet(connection, SP));
    }

    // =========================
    // DTO
    // =========================

    @Test
    void reportTabularDto_empty() {

        ReportTabularDto empty = ReportTabularDto.empty();

        assertFalse(empty.hasColumns());
        assertTrue(empty.getHeaders().isEmpty());
        assertTrue(empty.getRows().isEmpty());
    }
}
