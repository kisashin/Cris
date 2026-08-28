package co.com.bnpparibas.cardif.closingclaims.infraestructure.repository;

import org.hibernate.Session;
import org.hibernate.jdbc.ReturningWork;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.test.util.ReflectionTestUtils;

import javax.persistence.EntityManager;
import java.sql.CallableStatement;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class StoredProcedureExecutorTest {

    private static final String CALL = "EXEC dbo.sp_prueba";
    private static final String REQUIRED_COLUMN = "Familia";

    @Mock
    private EntityManager entityManager;

    @Mock
    private Session session;

    @Mock
    private Connection connection;

    @Mock
    private CallableStatement statement;

    @Mock
    private ResultSet resultSet;

    @Mock
    private ResultSetMetaData metaData;

    private StoredProcedureExecutor executor;

    @BeforeEach
    void setUp() {
        executor = new StoredProcedureExecutor();
        ReflectionTestUtils.setField(
                executor, "entityManager", entityManager);
        executor.setTimeoutSeconds(60);
    }

    @SuppressWarnings("unchecked")
    private void prepareSession() throws SQLException {
        when(entityManager.unwrap(Session.class)).thenReturn(session);
        when(session.doReturningWork(any(ReturningWork.class)))
                .thenAnswer(invocation -> {
                    ReturningWork<Object> work =
                            invocation.getArgument(0);
                    return work.execute(connection);
                });
        when(connection.prepareCall(anyString())).thenReturn(statement);
    }

    @Test
    @DisplayName("query mapea las filas del unico result set")
    void queryMapsRowsFromSingleResultSet() throws SQLException {
        prepareSession();

        when(statement.execute()).thenReturn(true);
        when(statement.getResultSet()).thenReturn(resultSet);
        when(resultSet.next()).thenReturn(true, true, false);
        when(resultSet.getString("valor")).thenReturn("uno", "dos");
        when(statement.getMoreResults()).thenReturn(false);
        when(statement.getUpdateCount()).thenReturn(-1);

        List<String> result = executor.query(
                CALL, rs -> rs.getString("valor"));

        assertEquals(2, result.size());
        assertEquals("uno", result.get(0));
        assertEquals("dos", result.get(1));

        verify(statement, times(1)).setQueryTimeout(60);
        verify(statement, times(1)).close();
        verify(resultSet, times(1)).close();
    }

    @Test
    @DisplayName("query recorre varios result sets")
    void queryReadsSeveralResultSets() throws SQLException {
        prepareSession();

        ResultSet second = mock(ResultSet.class);

        when(statement.execute()).thenReturn(true);
        when(statement.getResultSet()).thenReturn(resultSet, second);
        when(resultSet.next()).thenReturn(true, false);
        when(resultSet.getString("valor")).thenReturn("uno");
        when(second.next()).thenReturn(true, false);
        when(second.getString("valor")).thenReturn("dos");
        when(statement.getMoreResults()).thenReturn(true, false);
        when(statement.getUpdateCount()).thenReturn(-1);

        List<String> result = executor.query(
                CALL, rs -> rs.getString("valor"));

        assertEquals(2, result.size());
    }

    @Test
    @DisplayName("query devuelve lista vacia cuando no hay result sets")
    void queryReturnsEmptyListWhenThereAreNoResultSets()
            throws SQLException {
        prepareSession();

        when(statement.execute()).thenReturn(false);
        when(statement.getUpdateCount()).thenReturn(-1);

        List<String> result = executor.query(
                CALL, rs -> rs.getString("valor"));

        assertTrue(result.isEmpty());
        verify(statement, never()).getResultSet();
    }

    @Test
    @DisplayName("query omite los conteos de actualizacion")
    void querySkipsUpdateCounts() throws SQLException {
        prepareSession();

        when(statement.execute()).thenReturn(false);
        when(statement.getUpdateCount()).thenReturn(5, -1);
        when(statement.getMoreResults()).thenReturn(false);

        List<String> result = executor.query(
                CALL, rs -> rs.getString("valor"));

        assertTrue(result.isEmpty());
    }

    @Test
    @DisplayName("query filtrada mapea el result set que tiene la columna")
    void filteredQueryMapsMatchingResultSet() throws SQLException {
        prepareSession();

        when(statement.execute()).thenReturn(true);
        when(statement.getResultSet()).thenReturn(resultSet);
        when(resultSet.getMetaData()).thenReturn(metaData);
        when(metaData.getColumnCount()).thenReturn(2);
        when(metaData.getColumnLabel(1)).thenReturn("Otra");
        when(metaData.getColumnLabel(2)).thenReturn("familia");
        when(resultSet.next()).thenReturn(true, false);
        when(resultSet.getString("Familia")).thenReturn("ReasegAlfa");
        when(statement.getMoreResults()).thenReturn(false);
        when(statement.getUpdateCount()).thenReturn(-1);

        List<String> result = executor.query(
                CALL, rs -> rs.getString("Familia"), REQUIRED_COLUMN);

        assertEquals(1, result.size());
        assertEquals("ReasegAlfa", result.get(0));
        verify(resultSet, times(1)).close();
    }

    @Test
    @DisplayName("query filtrada descarta el result set sin la columna")
    void filteredQueryIgnoresResultSetWithoutColumn() throws SQLException {
        prepareSession();

        when(statement.execute()).thenReturn(true);
        when(statement.getResultSet()).thenReturn(resultSet);
        when(resultSet.getMetaData()).thenReturn(metaData);
        when(metaData.getColumnCount()).thenReturn(1);
        when(metaData.getColumnLabel(1)).thenReturn("Otra");
        when(statement.getMoreResults()).thenReturn(false);
        when(statement.getUpdateCount()).thenReturn(-1);

        List<String> result = executor.query(
                CALL, rs -> rs.getString("Familia"), REQUIRED_COLUMN);

        assertTrue(result.isEmpty());
        verify(resultSet, never()).next();
        verify(resultSet, times(1)).close();
    }

    @Test
    @DisplayName("query filtrada descarta el result set sin columnas")
    void filteredQueryIgnoresResultSetWithoutColumns() throws SQLException {
        prepareSession();

        when(statement.execute()).thenReturn(true);
        when(statement.getResultSet()).thenReturn(resultSet);
        when(resultSet.getMetaData()).thenReturn(metaData);
        when(metaData.getColumnCount()).thenReturn(0);
        when(statement.getMoreResults()).thenReturn(false);
        when(statement.getUpdateCount()).thenReturn(-1);

        List<String> result = executor.query(
                CALL, rs -> rs.getString("Familia"), REQUIRED_COLUMN);

        assertTrue(result.isEmpty());
    }

    @Test
    @DisplayName("query filtrada devuelve vacio cuando no hay result sets")
    void filteredQueryReturnsEmptyListWhenThereAreNoResultSets()
            throws SQLException {
        prepareSession();

        when(statement.execute()).thenReturn(false);
        when(statement.getUpdateCount()).thenReturn(-1);

        List<String> result = executor.query(
                CALL, rs -> rs.getString("Familia"), REQUIRED_COLUMN);

        assertTrue(result.isEmpty());
        verify(statement, never()).getResultSet();
    }

    @Test
    @DisplayName("setTimeoutSeconds aplica el valor configurado")
    void setTimeoutSecondsAppliesConfiguredValue() throws SQLException {
        prepareSession();

        executor.setTimeoutSeconds(120);

        when(statement.execute()).thenReturn(false);
        when(statement.getUpdateCount()).thenReturn(-1);

        executor.query(CALL, rs -> rs.getString("valor"));

        verify(statement, times(1)).setQueryTimeout(120);
    }
}
