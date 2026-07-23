package co.com.bnpparibas.cardif.cierres.infraestructure.repository.impl;

import java.math.BigDecimal;
import java.sql.CallableStatement;
import java.sql.ResultSet;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;
import javax.persistence.PersistenceContextType;

import org.hibernate.Session;
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

    private static final String SQL_ACCOUNTING_DATE =
            "SELECT dbo.fFecha2Txt(periodocontable,'') FROM parametro WHERE id = 4";
    private static final String SQL_ACCOUNTING_PERIOD =
            "SELECT dbo.fFecha2Txt(periodocontable,'/') FROM parametro WHERE id = 4";
    private static final String SQL_PRODUCTS =
            "SELECT Producto FROM patronxprod_siniestros ORDER BY Producto";
    private static final String SQL_LAYOUT =
            "SELECT COUNT(*) FROM patronxprod_siniestros WHERE producto = :product AND layout = 1";

    private static final String NO_XML = "0";

    @PersistenceContext(type = PersistenceContextType.EXTENDED)
    private EntityManager entityManager;

    @Override
    public String getAccountingDate() {
        return str(entityManager.createNativeQuery(SQL_ACCOUNTING_DATE).getSingleResult());
    }

    @Override
    public String getAccountingPeriodRaw() {
        return str(entityManager.createNativeQuery(SQL_ACCOUNTING_PERIOD).getSingleResult());
    }

    @Override
    public List<String> getProducts() {
        List<?> rows = entityManager.createNativeQuery(SQL_PRODUCTS).getResultList();

        return rows.stream()
                .map(ClaimAccountingRepositoryImpl::str)
                .collect(Collectors.toList());
    }

    @Override
    public int countProductLayout(String product) {
        Number total = (Number) entityManager.createNativeQuery(SQL_LAYOUT)
                .setParameter("product", product)
                .getSingleResult();

        return total.intValue();
    }

    @Override
    public String loadClaims(String product, boolean alpha) {
        try {
            List<Object[]> rows = callProcedure(alpha ? SP_CARGA_ALFA : SP_CARGA, product);

            return rows.isEmpty() ? "" : str(rows.get(0)[0]);
        } catch (Exception e) {
            log.error("Error ejecutando la carga de siniestros del producto {}", product, e);
            throw new DatabaseException(ExceptionConstants.DATABASE_CONNECTION, e);
        }
    }

    @Override
    public List<AccountingEntryRowDto> generateEntry(String comment, String product) {
        try {
            return callProcedure(SP_ASIENTO, 1, comment, product).stream()
                    .map(this::mapEntryRow)
                    .collect(Collectors.toList());
        } catch (Exception e) {
            log.error("Error generando el asiento del producto {}", product, e);
            throw new DatabaseException(ExceptionConstants.DATABASE_CONNECTION, e);
        }
    }

    @Override
    public List<AccountTotalRowDto> totalByAccount(String comment, String product) {
        try {
            return callProcedure(SP_ASIENTO, 3, comment, product).stream()
                    .map(this::mapTotalRow)
                    .collect(Collectors.toList());
        } catch (Exception e) {
            log.error("Error consultando el total por cuenta del producto {}", product, e);
            throw new DatabaseException(ExceptionConstants.DATABASE_CONNECTION, e);
        }
    }

    @Override
    public void registerEntry(String comment, String product) {
        try {
            callProcedure(SP_ASIENTO, 2, comment, product);
        } catch (Exception e) {
            log.error("Error registrando el asiento del producto {}", product, e);
            throw new DatabaseException(ExceptionConstants.DATABASE_CONNECTION, e);
        }
    }

    @Override
    public void markXmlGenerated(String comment, String product) {
        try {
            callProcedure(SP_ASIENTO, 4, comment, product);
        } catch (Exception e) {
            log.error("Error actualizando el estado del asiento del producto {}", product, e);
            throw new DatabaseException(ExceptionConstants.DATABASE_CONNECTION, e);
        }
    }

    @Override
    public String generateXml(String journalType, String period, String product, String comment) {
        try {
            List<Object[]> rows = callProcedure(SP_XML, journalType, period, product, comment);
            String xml = rows.isEmpty() ? "" : str(rows.get(0)[0]);

            return NO_XML.equals(xml) ? "" : xml;
        } catch (Exception e) {
            log.error("Error generando el XML {} del producto {}", journalType, product, e);
            throw new DatabaseException(ExceptionConstants.DATABASE_CONNECTION, e);
        }
    }

    /**
     * Ejecuta el procedimiento y devuelve las filas del ultimo conjunto de
     * resultados. Los procedimientos generan conteos de filas intermedios que
     * deben recorrerse antes de llegar a los datos.
     */
    private List<Object[]> callProcedure(String procedure, Object... parameters) {
        String call = buildCall(procedure, parameters.length);
        long start = System.currentTimeMillis();
        log.info("SP inicio {} params {}", procedure, Arrays.toString(parameters));

        List<Object[]> rows = entityManager.unwrap(Session.class).doReturningWork(connection -> {

            try (CallableStatement statement = connection.prepareCall(call)) {

                for (int i = 0; i < parameters.length; i++) {
                    statement.setObject(i + 1, parameters[i]);
                }

                List<Object[]> result = new ArrayList<>();
                boolean hasResultSet = statement.execute();

                while (hasResultSet || statement.getUpdateCount() != -1) {
                    if (hasResultSet) {
                        result.clear();
                        result.addAll(readRows(statement.getResultSet()));
                    }
                    hasResultSet = statement.getMoreResults();
                }

                return result;
            }
        });

        log.info("SP fin {} filas {} duracion {} ms",
                procedure, rows.size(), System.currentTimeMillis() - start);

        return rows;
    }

    private String buildCall(String procedure, int parameters) {
        StringBuilder placeholders = new StringBuilder();

        for (int i = 0; i < parameters; i++) {
            placeholders.append(i == 0 ? "?" : ",?");
        }

        return "{call " + procedure + "(" + placeholders + ")}";
    }

    private List<Object[]> readRows(ResultSet resultSet) throws java.sql.SQLException {
        List<Object[]> rows = new ArrayList<>();
        int columns = resultSet.getMetaData().getColumnCount();

        while (resultSet.next()) {
            Object[] row = new Object[columns];
            for (int i = 0; i < columns; i++) {
                row[i] = resultSet.getObject(i + 1);
            }
            rows.add(row);
        }

        return rows;
    }

    private AccountTotalRowDto mapTotalRow(Object[] row) {
        return AccountTotalRowDto.builder()
                .product(str(row[0]))
                .journalType(str(row[1]))
                .transactionReference(str(row[2]))
                .accountCode(str(row[3]))
                .debit(dec(row[4]))
                .credit(dec(row[5]))
                .build();
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
