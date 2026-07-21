package co.com.bnpparibas.cardif.cierres.infraestructure.repository.impl;

import java.math.BigDecimal;
import java.util.List;
import java.util.stream.Collectors;

import javax.persistence.EntityManager;
import javax.persistence.ParameterMode;
import javax.persistence.PersistenceContext;
import javax.persistence.PersistenceContextType;
import javax.persistence.StoredProcedureQuery;

import org.springframework.stereotype.Repository;

import co.com.bnpparibas.cardif.cierres.domain.dtos.AccountTotalRowDto;
import co.com.bnpparibas.cardif.cierres.domain.dtos.AccountingEntryRowDto;
import co.com.bnpparibas.cardif.cierres.domain.util.constants.ExceptionConstants;
import co.com.bnpparibas.cardif.cierres.domain.util.exception.DatabaseException;
import co.com.bnpparibas.cardif.cierres.infraestructure.repository.ClaimAccountingRepository;
import co.com.bnpparibas.webservicemask.repository.BNPRepository;

import lombok.extern.slf4j.Slf4j;

@Repository("claimAccountingRepositoryImpl")
@Slf4j
public class ClaimAccountingRepositoryImpl extends BNPRepository implements ClaimAccountingRepository {

    private static final String SP_ASIENTO = "[dbo].[sp_AsientoSiniestrosAdicionales]";
    private static final String SP_CARGA = "[dbo].[sp_CargaSiniestros]";
    private static final String SP_CARGA_ALFA = "[dbo].[sp_CargaSiniestrosAlfa]";
    private static final String SP_XML = "[dbo].[sp_XMLAsientosPru]";
    private static final String SP_LISTA_ARCHIVOS = "[dbo].[ListaArhivos]";

    private static final int ID_CORREO_ASIENTO = 6;

    private static final String NO_XML = "0";

    @PersistenceContext(type = PersistenceContextType.EXTENDED)
    private EntityManager entityManager;

    @Override
    public String getAccountingDate() {
        return String.valueOf(entityManager
                .createNativeQuery("SELECT dbo.fFecha2Txt(periodocontable,'') FROM parametro WHERE id = 4")
                .getSingleResult());
    }

    @Override
    public String getAccountingPeriodRaw() {
        return String.valueOf(entityManager
                .createNativeQuery("SELECT dbo.fFecha2Txt(periodocontable,'/') FROM parametro WHERE id = 4")
                .getSingleResult());
    }

    @Override
    public List<String> getProducts() {
        List<?> rows = entityManager
                .createNativeQuery("SELECT Producto FROM patronxprod_siniestros ORDER BY Producto")
                .getResultList();

        return rows.stream()
                .map(ClaimAccountingRepositoryImpl::str)
                .collect(Collectors.toList());
    }

    @Override
    public int countProductLayout(String product) {
        Number total = (Number) entityManager
                .createNativeQuery("SELECT COUNT(*) FROM patronxprod_siniestros WHERE producto = :product AND layout = 1")
                .setParameter("product", product)
                .getSingleResult();

        return total.intValue();
    }

    @Override
    public String loadClaims(String product, boolean alpha) {
        try {
            StoredProcedureQuery query = entityManager
                    .createStoredProcedureQuery(alpha ? SP_CARGA_ALFA : SP_CARGA);
            query.registerStoredProcedureParameter(1, String.class, ParameterMode.IN);
            query.setParameter(1, product);
            query.execute();

            List<?> rows = query.getResultList();

            return rows.isEmpty() ? "" : str(rows.get(0));
        } catch (Exception e) {
            throw new DatabaseException(ExceptionConstants.DATABASE_CONNECTION, e.getCause());
        }
    }

    @Override
    @SuppressWarnings("unchecked")
    public List<AccountingEntryRowDto> generateEntry(String comment, String product) {
        try {
            StoredProcedureQuery query = accountingEntryQuery(1, comment, product);
            query.execute();

            List<Object[]> rows = query.getResultList();

            return rows.stream()
                    .map(this::mapEntryRow)
                    .collect(Collectors.toList());
        } catch (Exception e) {
            throw new DatabaseException(ExceptionConstants.DATABASE_CONNECTION, e.getCause());
        }
    }

    @Override
    @SuppressWarnings("unchecked")
    public List<AccountTotalRowDto> totalByAccount(String comment, String product) {
        try {
            StoredProcedureQuery query = accountingEntryQuery(3, comment, product);
            query.execute();

            List<Object[]> rows = query.getResultList();

            return rows.stream()
                    .map(row -> AccountTotalRowDto.builder()
                            .product(str(row[0]))
                            .journalType(str(row[1]))
                            .transactionReference(str(row[2]))
                            .accountCode(str(row[3]))
                            .debit(dec(row[4]))
                            .credit(dec(row[5]))
                            .build())
                    .collect(Collectors.toList());
        } catch (Exception e) {
            throw new DatabaseException(ExceptionConstants.DATABASE_CONNECTION, e.getCause());
        }
    }

    @Override
    public void registerEntry(String comment, String product) {
        try {
            accountingEntryQuery(2, comment, product).execute();
        } catch (Exception e) {
            throw new DatabaseException(ExceptionConstants.DATABASE_CONNECTION, e.getCause());
        }
    }

    @Override
    public void markXmlGenerated(String comment, String product) {
        try {
            accountingEntryQuery(4, comment, product).execute();
        } catch (Exception e) {
            throw new DatabaseException(ExceptionConstants.DATABASE_CONNECTION, e.getCause());
        }
    }

    @Override
    public String generateXml(String journalType, String period, String product, String comment) {
        try {
            StoredProcedureQuery query = entityManager.createStoredProcedureQuery(SP_XML);
            query.registerStoredProcedureParameter(1, String.class, ParameterMode.IN);
            query.registerStoredProcedureParameter(2, String.class, ParameterMode.IN);
            query.registerStoredProcedureParameter(3, String.class, ParameterMode.IN);
            query.registerStoredProcedureParameter(4, String.class, ParameterMode.IN);
            query.setParameter(1, journalType);
            query.setParameter(2, period);
            query.setParameter(3, product);
            query.setParameter(4, comment);
            query.execute();

            List<?> rows = query.getResultList();
            String xml = rows.isEmpty() ? "" : str(rows.get(0));

            return NO_XML.equals(xml) ? "" : xml;
        } catch (Exception e) {
            throw new DatabaseException(ExceptionConstants.DATABASE_CONNECTION, e.getCause());
        }
    }

    @Override
    public void notifyByMail(String xmlName, String userName, String body) {
        try {
            StoredProcedureQuery query = entityManager.createStoredProcedureQuery(SP_LISTA_ARCHIVOS);
            query.registerStoredProcedureParameter(1, Integer.class, ParameterMode.IN);
            query.registerStoredProcedureParameter(2, String.class, ParameterMode.IN);
            query.registerStoredProcedureParameter(3, String.class, ParameterMode.IN);
            query.registerStoredProcedureParameter(4, String.class, ParameterMode.IN);
            query.setParameter(1, ID_CORREO_ASIENTO);
            query.setParameter(2, xmlName);
            query.setParameter(3, userName);
            query.setParameter(4, body);
            query.execute();
        } catch (Exception e) {
            throw new DatabaseException(ExceptionConstants.DATABASE_CONNECTION, e.getCause());
        }
    }

    private StoredProcedureQuery accountingEntryQuery(int mode, String comment, String product) {
        StoredProcedureQuery query = entityManager.createStoredProcedureQuery(SP_ASIENTO);
        query.registerStoredProcedureParameter(1, Integer.class, ParameterMode.IN);
        query.registerStoredProcedureParameter(2, String.class, ParameterMode.IN);
        query.registerStoredProcedureParameter(3, String.class, ParameterMode.IN);
        query.setParameter(1, mode);
        query.setParameter(2, comment);
        query.setParameter(3, product);

        return query;
    }

    /**
     * El procedimiento no asigna alias a varias columnas, por lo que el mapeo es
     * posicional y depende del orden del SELECT.
     */
    private AccountingEntryRowDto mapEntryRow(Object[] row) {
        return AccountingEntryRowDto.builder()
                .journalType(str(row[0]))
                .accountingPeriod(str(row[1]))
                .transactionDate(str(row[2]))
                .accountCode(str(row[3]))
                .transactionReference(str(row[4]))
                .description(str(row[5]))
                .dueDate(str(row[6]))
                .currencyCode(str(row[7]))
                .transactionAmount(dec(row[8]))
                .baseAmount(str(row[9]))
                .debitCredit(str(row[10]))
                .costCenter(str(row[11]))
                .product(str(row[12]))
                .branch(str(row[13]))
                .tax(str(row[14]))
                .partner(str(row[15]))
                .nit(str(row[16]))
                .advisorKey(str(row[17]))
                .coverage(str(row[18]))
                .xDefine(str(row[19]))
                .planId(str(row[20]))
                .journalSource(str(row[21]))
                .format(str(row[22]))
                .processDate(str(row[23]))
                .entryDescription(str(row[24]))
                .status(str(row[25]))
                .claimNumber(str(row[26]))
                .build();
    }

    private static String str(Object value) {
        return value == null ? null : String.valueOf(value);
    }

    private static BigDecimal dec(Object value) {
        return value == null ? null : new BigDecimal(String.valueOf(value));
    }
}
