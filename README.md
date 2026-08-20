package co.com.bnpparibas.cardif.closingclaims.infraestructure.repository;

import org.hibernate.Session;
import org.springframework.stereotype.Repository;

import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;
import java.sql.CallableStatement;

@Repository
public class CardifPeruAccountingProcedureRepository {

    private static final String PROCEDURE_CALL =
            "{call dbo.sp_contabiliza_cardif_ext}";

    @PersistenceContext
    private EntityManager entityManager;

    public void executeAccountingProcedure(int timeoutSeconds) {
        entityManager.unwrap(Session.class).doWork(connection -> {
            try (CallableStatement statement =
                         connection.prepareCall(PROCEDURE_CALL)) {

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
}
