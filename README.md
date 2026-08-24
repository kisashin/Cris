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
import java.sql.SQLException;
import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class StoredProcedureExecutorTest {

    private static final String CALL = "EXEC dbo.sp_test";
    private static final int TIMEOUT = 180;

    @Mock
    private EntityManager entityManager;

    @Mock
    private Session session;

    @Mock
    private Connection connection;

    @Mock
    private CallableStatement statement;

    private StoredProcedureExecutor executor;

    @BeforeEach
    void setUp() throws SQLException {
        executor = new StoredProcedureExecutor();
        ReflectionTestUtils.setField(
                executor, "entityManager", entityManager);
        executor.setTimeoutSeconds(TIMEOUT);

        when(entityManager.unwrap(Session.class)).thenReturn(session);
        when(connection.prepareCall(anyString())).thenReturn(statement);
    }

    @Test
    @DisplayName("Should map every row and close the result set")
    void shouldMapEveryRowAndCloseResultSet() throws SQLException {
        ResultSet resultSet = mock(ResultSet.class);

        when(statement.execute()).thenReturn(true);
        when(statement.getResultSet()).thenReturn(resultSet);
        when(statement.getUpdateCount()).thenReturn(-1);
        when(statement.getMoreResults()).thenReturn(false);
        when(resultSet.next()).thenReturn(true, true, false);
        when(resultSet.getString("Line"))
                .thenReturn("<Line>1</Line>", "<Line>2</Line>");

        mockReturningWork();

        List<String> rows = executor.query(
                CALL, row -> row.getString("Line"));

        assertEquals(
                Arrays.asList("<Line>1</Line>", "<Line>2</Line>"), rows);

        verify(statement).setQueryTimeout(TIMEOUT);
        verify(resultSet).close();
        verify(statement).close();
    }

    @Test
    @DisplayName("Should return an empty list when there is no result set")
    void shouldReturnEmptyListWhenThereIsNoResultSet() throws SQLException {
        when(statement.execute()).thenReturn(false);
        when(statement.getUpdateCount()).thenReturn(-1);

        mockReturningWork();

        assertTrue(executor.query(CALL, row -> row.getString("Line")).isEmpty());
        verify(statement).close();
    }

    @Test
    @DisplayName("Should propagate errors raised by the mapper")
    void shouldPropagateMapperErrors() throws SQLException {
        ResultSet resultSet = mock(ResultSet.class);

        when(statement.execute()).thenReturn(true);
        when(statement.getResultSet()).thenReturn(resultSet);
        when(resultSet.next()).thenReturn(true);

        mockReturningWork();

        assertThrows(
                IllegalStateException.class,
                () -> executor.query(CALL, row -> {
                    throw new IllegalStateException("mapper error");
                }));
    }

    @SuppressWarnings("unchecked")
    private void mockReturningWork() {
        when(session.doReturningWork(any(ReturningWork.class)))
                .thenAnswer(invocation -> invocation
                        .getArgument(0, ReturningWork.class)
                        .execute(connection));
    }
}
