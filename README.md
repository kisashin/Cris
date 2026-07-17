ClaimAccountingRepositoryImpl

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

/**
 * Acceso a datos de Asientos Siniestros (reaseguro).
 *
 * Patrón de la casa: extiende BNPRepository y usa entityManager directo, igual
 * que MatrizCondicionesRepositoryImpl. NO se usa invokeQuery/BNPQuery porque eso
 * es solo para SP de salida escalar (Novelty); estos SP legacy devuelven
 * RESULTSET crudo, así que se leen con createStoredProcedureQuery + getResultList
 * y se mapea Object[] posicional (como getAllMatrizCondiciones).
 *
 * IMPORTANTE: no se toca ningún SP. sp_XMLAsientosPru sigue intentando escribir
 * el archivo por bcp/xp_cmdshell; ese efecto se ignora (ver ServiceImpl) porque
 * el archivo bueno lo entrega Spring con el string que aquí se captura.
 */
@Repository("claimAccountingRepositoryImpl")
@Slf4j
public class ClaimAccountingRepositoryImpl extends BNPRepository implements ClaimAccountingRepository {

    @PersistenceContext(type = PersistenceContextType.EXTENDED)
    private EntityManager entityManager;

    // ---------- lecturas simples (patrón createNativeQuery) ----------

    /** fFecha2Txt(...,'') => YYYYMMDD (el front lo corta con substring(0,6)). */
    @Override
    public String getAccountingDate() {
        return (String) entityManager
                .createNativeQuery("SELECT dbo.fFecha2Txt(periodocontable,'') FROM parametro WHERE id = 4")
                .getSingleResult();
    }

    /** fFecha2Txt(...,'/') => YYYY/MM/DD. Base para armar el periodo canónico YYYY/0MM. */
    @Override
    public String getAccountingPeriodRaw() {
        return (String) entityManager
                .createNativeQuery("SELECT dbo.fFecha2Txt(periodocontable,'/') FROM parametro WHERE id = 4")
                .getSingleResult();
    }

    @Override
    @SuppressWarnings("unchecked")
    public List<String> getProducts() {
        return entityManager
                .createNativeQuery("SELECT Producto FROM patronxprod_siniestros ORDER BY Producto")
                .getResultList();
    }

    @Override
    public int countProductLayout(String product) {
        Number n = (Number) entityManager
                .createNativeQuery("SELECT COUNT(*) FROM patronxprod_siniestros WHERE producto = :p AND layout = 1")
                .setParameter("p", product)
                .getSingleResult();
        return n.intValue();
    }

    // ---------- Cargar: SP con xp_cmdshell + BULK, devuelve UN mensaje como resultset ----------

    /**
     * @param alpha true => sp_CargaSiniestrosAlfa (layout=1), false => sp_CargaSiniestros.
     * @return el mensaje inline del SP ('N Registros Cargados...' o 'No hay archivo de siniestros').
     */
    @Override
    public String loadClaims(String product, boolean alpha) {
        String sp = alpha ? "[dbo].[sp_CargaSiniestrosAlfa]" : "[dbo].[sp_CargaSiniestros]";
        try {
            StoredProcedureQuery q = entityManager.createStoredProcedureQuery(sp);
            q.registerStoredProcedureParameter(1, String.class, ParameterMode.IN); // @Producto
            q.setParameter(1, product);
            q.execute();
            List<?> rows = q.getResultList();          // resultset de 1 columna => List<String>
            return rows.isEmpty() ? "" : String.valueOf(rows.get(0));
        } catch (Exception e) {
            throw new DatabaseException(ExceptionConstants.DATABASE_CONNECTION, e.getCause());
        }
    }

    // ---------- Generar (modo 1): resultset de 27 columnas ----------

    @Override
    @SuppressWarnings("unchecked")
    public List<AccountingEntryRowDto> generateEntry(String comment, String product) {
        try {
            StoredProcedureQuery q = spAsiento(1, comment, product);
            q.execute();
            List<Object[]> rows = q.getResultList();
            return rows.stream().map(this::mapEntryRow).collect(Collectors.toList());
        } catch (Exception e) {
            throw new DatabaseException(ExceptionConstants.DATABASE_CONNECTION, e.getCause());
        }
    }

    // ---------- Total x Cuenta (modo 3): resultset de 6 columnas ----------

    @Override
    @SuppressWarnings("unchecked")
    public List<AccountTotalRowDto> totalByAccount(String comment, String product) {
        try {
            StoredProcedureQuery q = spAsiento(3, comment, product);
            q.execute();
            List<Object[]> rows = q.getResultList();
            return rows.stream()
                    .map(r -> AccountTotalRowDto.builder()
                            .product(str(r[0]))
                            .journalType(str(r[1]))
                            .transactionReference(str(r[2]))
                            .accountCode(str(r[3]))
                            .debit(dec(r[4]))
                            .credit(dec(r[5]))
                            .build())
                    .collect(Collectors.toList());
        } catch (Exception e) {
            throw new DatabaseException(ExceptionConstants.DATABASE_CONNECTION, e.getCause());
        }
    }

    // ---------- Registrar (modo 2): DML, sin resultset ----------

    @Override
    public void registerEntry(String comment, String product) {
        try {
            spAsiento(2, comment, product).execute(); // internamente: insert into ha exec ...modo 1
        } catch (Exception e) {
            throw new DatabaseException(ExceptionConstants.DATABASE_CONNECTION, e.getCause());
        }
    }

    // ---------- Marcar XML generado (modo 4): DML ----------

    @Override
    public void markXmlGenerated(String comment, String product) {
        try {
            spAsiento(4, comment, product).execute();
        } catch (Exception e) {
            throw new DatabaseException(ExceptionConstants.DATABASE_CONNECTION, e.getCause());
        }
    }

    // ---------- XML por tipo de diario (SINIE / LRVSI / CRVSI) ----------

    /**
     * Captura el resultset dataXml de sp_XMLAsientosPru. El SP además muta ~40 veces
     * HistoricoAsientosPru e intenta escribir por bcp: eso se deja correr y se ignora.
     * @return el XML, o "" si el SP devolvió '0' (no hay asientos de ese tipo).
     */
    @Override
    public String generateXml(String journalType, String period, String product, String comment) {
        try {
            StoredProcedureQuery q = entityManager.createStoredProcedureQuery("[dbo].[sp_XMLAsientosPru]");
            q.registerStoredProcedureParameter(1, String.class, ParameterMode.IN); // @Tipo_Diario
            q.registerStoredProcedureParameter(2, String.class, ParameterMode.IN); // @Periodo_Contable
            q.registerStoredProcedureParameter(3, String.class, ParameterMode.IN); // @Producto
            q.registerStoredProcedureParameter(4, String.class, ParameterMode.IN); // @ajuste
            // @XmlDestino (5º) tiene default 'SUN'; se omite. Si el driver exige todos
            // los params, registrar el 5º y pasar "SUN".
            q.setParameter(1, journalType);
            q.setParameter(2, period);
            q.setParameter(3, product);
            q.setParameter(4, comment);
            q.execute();
            List<?> rows = q.getResultList(); // 1 columna => List<String>
            String xml = rows.isEmpty() ? "" : String.valueOf(rows.get(0));
            return "0".equals(xml) ? "" : xml;
        } catch (Exception e) {
            throw new DatabaseException(ExceptionConstants.DATABASE_CONNECTION, e.getCause());
        }
    }

    // ---------- Correo (ListaArhivos id=6): Database Mail server-side ----------

    @Override
    public void notifyByMail(String xmlName, String userName, String body) {
        try {
            StoredProcedureQuery q = entityManager.createStoredProcedureQuery("[dbo].[ListaArhivos]");
            q.registerStoredProcedureParameter(1, Integer.class, ParameterMode.IN); // @id = 6
            q.registerStoredProcedureParameter(2, String.class, ParameterMode.IN);  // @Archivo
            q.registerStoredProcedureParameter(3, String.class, ParameterMode.IN);  // @Us (usuario)
            q.registerStoredProcedureParameter(4, String.class, ParameterMode.IN);  // @body
            q.setParameter(1, 6);
            q.setParameter(2, xmlName);
            q.setParameter(3, userName);
            q.setParameter(4, body);
            q.execute();
        } catch (Exception e) {
            throw new DatabaseException(ExceptionConstants.DATABASE_CONNECTION, e.getCause());
        }
    }

    // ================= helpers =================

    private StoredProcedureQuery spAsiento(int mode, String comment, String product) {
        StoredProcedureQuery q = entityManager.createStoredProcedureQuery("[dbo].[sp_AsientoSiniestrosAdicionales]");
        q.registerStoredProcedureParameter(1, Integer.class, ParameterMode.IN); // @id
        q.registerStoredProcedureParameter(2, String.class, ParameterMode.IN);  // @ComentarioAsiento
        q.registerStoredProcedureParameter(3, String.class, ParameterMode.IN);  // @Producto
        q.setParameter(1, mode);
        q.setParameter(2, comment);
        q.setParameter(3, product);
        return q;
    }

    /**
     * Modo 1 => 27 columnas en el ORDEN EXACTO del SELECT del SP. El SP no pone alias
     * en varias columnas, así que el mapeo es POSICIONAL, no por nombre. Si alguien
     * reordena el SELECT del SP, este mapeo se rompe: hay que blindarlo con un test.
     */
    private AccountingEntryRowDto mapEntryRow(Object[] r) {
        return AccountingEntryRowDto.builder()
                .journalType(str(r[0]))              // cu.tipodiario
                .accountingPeriod(str(r[1]))         // Periodo_contable
                .transactionDate(str(r[2]))          // Fecha_transaccion
                .accountCode(str(r[3]))              // cu.cuenta
                .transactionReference(str(r[4]))     // REF_TRANSACCION
                .description(str(r[5]))              // SO.DESCRIPCION
                .dueDate(str(r[6]))                  // Fecha_Vencimiento
                .currencyCode(str(r[7]))             // 'COP'
                .transactionAmount(dec(r[8]))        // Importe_Transaccion
                .baseAmount(str(r[9]))               // '0'
                .debitCredit(str(r[10]))             // cu.naturaleza
                .costCenter(str(r[11]))              // '99999'
                .product(str(r[12]))                 // co.producto
                .branch(str(r[13]))                  // co.ramo
                .tax(str(r[14]))                     // '99'
                .partner(str(r[15]))                 // socio
                .nit(str(r[16]))                     // so.nit
                .advisorKey(str(r[17]))              // '9999999'
                .coverage(str(r[18]))                // co.cobertura
                .xDefine(str(r[19]))                 // '0'
                .planId(str(r[20]))                  // '99999'
                .journalSource(str(r[21]))           // 'SSC'
                .format(str(r[22]))                  // '1;2'
                .processDate(str(r[23]))             // Fecha_proceso
                .entryDescription(str(r[24]))        // @ComentarioAsiento
                .status(str(r[25]))                  // 'Pendiente XML'
                .claimNumber(str(r[26]))             // Siniestro
                .build();
    }

    private static String str(Object o) {
        return o == null ? null : o.toString();
    }

    private static BigDecimal dec(Object o) {
        return o == null ? null : new BigDecimal(o.toString());
    }
}
