package co.com.bnpparibas.cardif.closingclaims.infraestructure.repository;

import org.hibernate.Session;
import org.hibernate.jdbc.Work;
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

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class CardifPeruAccountingProcedureRepositoryTest {

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

    private CardifPeruAccountingProcedureRepository repository;

    @BeforeEach
    void setUp() {
        repository = new CardifPeruAccountingProcedureRepository();
        ReflectionTestUtils.setField(
                repository, "entityManager", entityManager);
    }

    private void prepareSession() throws SQLException {
        when(entityManager.unwrap(Session.class)).thenReturn(session);
        doAnswerWork();
        when(connection.prepareCall(anyString())).thenReturn(statement);
    }

    private void doAnswerWork() {
        org.mockito.Mockito.doAnswer(invocation -> {
            Work work = invocation.getArgument(0);
            work.execute(connection);
            return null;
        }).when(session).doWork(any(Work.class));
    }

    @Test
    @DisplayName("debe ejecutar el procedimiento y cerrar los cursores")
    void shouldExecuteProcedureAndCloseResultSets() throws SQLException {
        prepareSession();

        when(statement.execute()).thenReturn(true);
        when(statement.getResultSet()).thenReturn(resultSet);
        when(statement.getMoreResults()).thenReturn(false);
        when(statement.getUpdateCount()).thenReturn(-1);

        repository.executeAccountingProcedure(180);

        verify(statement, times(1)).setQueryTimeout(180);
        verify(statement, times(1)).execute();
        verify(resultSet, times(1)).close();
        verify(statement, times(1)).close();
    }

    @Test
    @DisplayName("debe recorrer varios result sets")
    void shouldIterateSeveralResultSets() throws SQLException {
        prepareSession();

        ResultSet second = org.mockito.Mockito.mock(ResultSet.class);

        when(statement.execute()).thenReturn(true);
        when(statement.getResultSet()).thenReturn(resultSet, second);
        when(statement.getMoreResults()).thenReturn(true, false);
        when(statement.getUpdateCount()).thenReturn(-1);

        repository.executeAccountingProcedure(120);

        verify(resultSet, times(1)).close();
        verify(second, times(1)).close();
        verify(statement, times(1)).setQueryTimeout(120);
    }

    @Test
    @DisplayName("debe terminar cuando el procedimiento no devuelve result sets")
    void shouldFinishWhenThereAreNoResultSets() throws SQLException {
        prepareSession();

        when(statement.execute()).thenReturn(false);
        when(statement.getUpdateCount()).thenReturn(-1);

        repository.executeAccountingProcedure(60);

        verify(statement, never()).getResultSet();
        verify(statement, times(1)).close();
    }

    @Test
    @DisplayName("debe omitir los conteos de actualizacion")
    void shouldSkipUpdateCounts() throws SQLException {
        prepareSession();

        when(statement.execute()).thenReturn(false);
        when(statement.getUpdateCount()).thenReturn(5, -1);
        when(statement.getMoreResults()).thenReturn(false);

        repository.executeAccountingProcedure(60);

        verify(statement, never()).getResultSet();
        verify(statement, times(1)).close();
    }
}
