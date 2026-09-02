package co.com.bnpparibas.cardif.repository.imp;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyInt;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.sql.CallableStatement;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

import javax.persistence.EntityManager;
import javax.persistence.Query;

import org.hibernate.Session;
import org.hibernate.jdbc.ReturningWork;
import org.hibernate.jdbc.Work;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.mockito.junit.jupiter.MockitoSettings;
import org.mockito.quality.Strictness;

import co.com.bnpparibas.cardif.builders.ClaimAccountingBuilder;
import co.com.bnpparibas.cardif.cierres.domain.dtos.AccountTotalRowDto;
import co.com.bnpparibas.cardif.cierres.domain.dtos.AccountingEntryRowDto;
import co.com.bnpparibas.cardif.cierres.domain.dtos.AccountingFileDto;
import co.com.bnpparibas.cardif.cierres.domain.dtos.DownloadFileDto;
import co.com.bnpparibas.cardif.cierres.domain.dtos.XmlFileDto;
import co.com.bnpparibas.cardif.cierres.domain.util.exception.DatabaseException;
import co.com.bnpparibas.cardif.cierres.domain.util.helpers.ClaimFileHelper;
import co.com.bnpparibas.cardif.cierres.infraestructure.repository.impl.ClaimAccountingRepositoryImpl;

@ExtendWith(MockitoExtension.class)
@MockitoSettings(strictness = Strictness.LENIENT)
class ClaimAccountingRepositoryImplTest {

    @InjectMocks
    private ClaimAccountingRepositoryImpl repository;

    @Mock
    private EntityManager entityManager;

    @Mock
    private Session session;

    @Mock
    private Connection connection;

    @Mock
    private CallableStatement statement;

    @Mock
    private PreparedStatement preparedStatement;

    @Mock
    private ResultSet resultSet;

    @Mock
    private ResultSetMetaData metaData;

    @Mock
    private Query query;

    private void mockNativeQuery(Object singleResult, List<?> resultList) {
        when(entityManager.createNativeQuery(anyString())).thenReturn(query);
        when(query.setParameter(anyString(), any())).thenReturn(query);
        when(query.getSingleResult()).thenReturn(singleResult);
        when(query.getResultList()).thenReturn(resultList);
        when(query.executeUpdate()).thenReturn(1);
    }

    private void mockBatch() throws SQLException {
        when(entityManager.unwrap(Session.class)).thenReturn(session);
        when(connection.prepareStatement(anyString())).thenReturn(preparedStatement);

        org.mockito.Mockito.doAnswer(invocation -> {
            Work work = invocation.getArgument(0);
            work.execute(connection);
            return null;
        }).when(session).doWork(any());
    }

    private void mockProcedure(Object[]... rows) throws SQLException {
        when(entityManager.unwrap(Session.class)).thenReturn(session);
        when(session.doReturningWork(any())).thenAnswer(invocation -> {
            ReturningWork<?> work = invocation.getArgument(0);
            return work.execute(connection);
        });
        when(connection.prepareCall(anyString())).thenReturn(statement);
        when(statement.execute()).thenReturn(true);
        when(statement.getResultSet()).thenReturn(resultSet);
        when(statement.getMoreResults()).thenReturn(false);
        when(statement.getUpdateCount()).thenReturn(-1);
        when(resultSet.getMetaData()).thenReturn(metaData);

        if (rows.length == 0) {
            when(metaData.getColumnCount()).thenReturn(1);
            when(resultSet.next()).thenReturn(false);
            return;
        }

        when(metaData.getColumnCount()).thenReturn(rows[0].length);

        Boolean[] remaining = new Boolean[rows.length];
        Arrays.fill(remaining, Boolean.TRUE);
        when(resultSet.next()).thenReturn(Boolean.TRUE, appendFalse(remaining));

        when(resultSet.getObject(anyInt())).thenAnswer(invocation -> {
            int column = invocation.getArgument(0);
            return rows[0][column - 1];
        });
    }

    private Boolean[] appendFalse(Boolean[] values) {
        Boolean[] result = Arrays.copyOf(values, values.length);
        result[values.length - 1] = Boolean.FALSE;
        return result;
    }

    private List<String[]> tempRows(int total) {
        List<String[]> rows = new ArrayList<>();

        for (int i = 0; i < total; i++) {
            String[] row = new String[ClaimFileHelper.COLUMNS];
            Arrays.fill(row, "V");
            rows.add(row);
        }

        return rows;
    }

    @Test
    void getAccountingDate_devuelveElValorDeLaFuncion() {
        mockNativeQuery("20260201", null);

        assertEquals("20260201", repository.getAccountingDate());
    }

    @Test
    void getAccountingPeriodRaw_devuelveElValorConSeparador() {
        mockNativeQuery("2026/02/01", null);

        assertEquals("2026/02/01", repository.getAccountingPeriodRaw());
    }

    @Test
    void getProducts_convierteLosValoresNumericosATexto() {
        mockNativeQuery(null, Arrays.asList(2012, 2028));

        List<String> products = repository.getProducts();

        assertEquals(2, products.size());
        assertTrue(products.contains("2012"));
    }

    @Test
    void findPattern_devuelveElPatronDelProducto() {
        mockNativeQuery(null, Collections.singletonList(ClaimAccountingBuilder.PATTERN));

        assertEquals(ClaimAccountingBuilder.PATTERN,
                repository.findPattern(ClaimAccountingBuilder.PRODUCT));
    }

    @Test
    void findPattern_sinResultadoDevuelveNulo() {
        mockNativeQuery(null, Collections.emptyList());

        assertNull(repository.findPattern("9999"));
    }

    @Test
    void clearTempClaims_ejecutaElBorrado() {
        mockNativeQuery(null, null);

        repository.clearTempClaims();

        verify(query).executeUpdate();
    }

    @Test
    void insertTempClaims_agregaCadaFilaAlLote() throws SQLException {
        mockBatch();

        repository.insertTempClaims(tempRows(3));

        verify(preparedStatement, times(3)).addBatch();
        verify(preparedStatement).executeBatch();
    }

    @Test
    void insertTempClaims_ejecutaUnLoteIntermedioAlSuperarElTamano() throws SQLException {
        mockBatch();

        repository.insertTempClaims(tempRows(150));

        verify(preparedStatement, times(150)).addBatch();
        verify(preparedStatement, times(2)).executeBatch();
    }

    @Test
    void insertTempClaims_sinFilasNoAgregaNada() throws SQLException {
        mockBatch();

        repository.insertTempClaims(new ArrayList<>());

        verify(preparedStatement, times(0)).addBatch();
        verify(preparedStatement).executeBatch();
    }

    @Test
    void loadClaims_devuelveElMensajeDelProcedimiento() throws SQLException {
        mockProcedure(new Object[] { "119 Registros Cargados" });

        assertEquals("119 Registros Cargados",
                repository.loadClaims(ClaimAccountingBuilder.PRODUCT, ClaimAccountingBuilder.CSV_NAME));
    }

    @Test
    void loadClaims_sinResultadoDevuelveVacio() throws SQLException {
        mockProcedure();

        assertEquals("",
                repository.loadClaims(ClaimAccountingBuilder.PRODUCT, ClaimAccountingBuilder.CSV_NAME));
    }

    @Test
    void loadClaims_propagaElErrorComoExcepcionDeBase() {
        when(entityManager.unwrap(Session.class)).thenThrow(new IllegalStateException());

        assertThrows(DatabaseException.class,
                () -> repository.loadClaims(ClaimAccountingBuilder.PRODUCT, ClaimAccountingBuilder.CSV_NAME));
    }

    @Test
    void generateEntry_mapeaLasVeintisieteColumnasEnOrden() throws SQLException {
        mockProcedure(ClaimAccountingBuilder.entryRow());

        List<AccountingEntryRowDto> rows =
                repository.generateEntry(ClaimAccountingBuilder.COMMENT, ClaimAccountingBuilder.PRODUCT);

        assertEquals(1, rows.size());
        AccountingEntryRowDto row = rows.get(0);
        assertEquals("SINIE", row.getJournalType());
        assertEquals("51144000", row.getAccountCode());
        assertEquals("Pago Definitivo", row.getTransactionReference());
        assertEquals("D", row.getDebitCredit());
        assertEquals("2012", row.getProduct());
        assertEquals("SIN-001", row.getClaimNumber());
        assertEquals(0, row.getTransactionAmount().compareTo(new java.math.BigDecimal("150000")));
    }

    @Test
    void generateEntry_propagaElErrorComoExcepcionDeBase() {
        when(entityManager.unwrap(Session.class)).thenThrow(new IllegalStateException());

        assertThrows(DatabaseException.class,
                () -> repository.generateEntry(ClaimAccountingBuilder.COMMENT, ClaimAccountingBuilder.PRODUCT));
    }

    @Test
    void totalByAccount_mapeaLasSeisColumnas() throws SQLException {
        mockProcedure(ClaimAccountingBuilder.totalRow());

        List<AccountTotalRowDto> rows =
                repository.totalByAccount(ClaimAccountingBuilder.COMMENT, ClaimAccountingBuilder.PRODUCT);

        assertEquals(1, rows.size());
        AccountTotalRowDto row = rows.get(0);
        assertEquals("2012", row.getProduct());
        assertEquals("SINIE", row.getJournalType());
        assertEquals("51144000", row.getAccountCode());
        assertEquals(0, row.getDebit().compareTo(new java.math.BigDecimal("150000")));
        assertEquals(0, row.getCredit().compareTo(java.math.BigDecimal.ZERO));
    }

    @Test
    void totalByAccount_propagaElErrorComoExcepcionDeBase() {
        when(entityManager.unwrap(Session.class)).thenThrow(new IllegalStateException());

        assertThrows(DatabaseException.class,
                () -> repository.totalByAccount(ClaimAccountingBuilder.COMMENT, ClaimAccountingBuilder.PRODUCT));
    }

    @Test
    void registerEntry_ejecutaElProcedimiento() throws SQLException {
        mockProcedure();

        repository.registerEntry(ClaimAccountingBuilder.COMMENT, ClaimAccountingBuilder.PRODUCT);

        verify(statement).execute();
    }

    @Test
    void registerEntry_propagaElErrorComoExcepcionDeBase() {
        when(entityManager.unwrap(Session.class)).thenThrow(new IllegalStateException());

        assertThrows(DatabaseException.class,
                () -> repository.registerEntry(ClaimAccountingBuilder.COMMENT, ClaimAccountingBuilder.PRODUCT));
    }

    @Test
    void markXmlGenerated_ejecutaElProcedimiento() throws SQLException {
        mockProcedure();

        repository.markXmlGenerated(ClaimAccountingBuilder.COMMENT, ClaimAccountingBuilder.PRODUCT);

        verify(statement).execute();
    }

    @Test
    void markXmlGenerated_propagaElErrorComoExcepcionDeBase() {
        when(entityManager.unwrap(Session.class)).thenThrow(new IllegalStateException());

        assertThrows(DatabaseException.class,
                () -> repository.markXmlGenerated(ClaimAccountingBuilder.COMMENT, ClaimAccountingBuilder.PRODUCT));
    }

    @Test
    void generateXml_devuelveTipoNombreYContenido() throws SQLException {
        mockProcedure(ClaimAccountingBuilder.xmlRow());

        XmlFileDto file = repository.generateXml("SINIE", ClaimAccountingBuilder.PERIOD,
                ClaimAccountingBuilder.PRODUCT, ClaimAccountingBuilder.COMMENT);

        assertEquals("SINIE", file.getJournalType());
        assertEquals(ClaimAccountingBuilder.FILE_NAME, file.getFileName());
        assertEquals(ClaimAccountingBuilder.XML_CONTENT, file.getContent());
    }

    @Test
    void generateXml_traduceElIndicadorSinAsientosANulo() throws SQLException {
        mockProcedure(new Object[] { "LRVSI", ClaimAccountingBuilder.FILE_NAME, "0" });

        assertNull(repository.generateXml("LRVSI", ClaimAccountingBuilder.PERIOD,
                ClaimAccountingBuilder.PRODUCT, ClaimAccountingBuilder.COMMENT));
    }

    @Test
    void generateXml_conContenidoNuloDevuelveNulo() throws SQLException {
        mockProcedure(new Object[] { "CRVSI", ClaimAccountingBuilder.FILE_NAME, null });

        assertNull(repository.generateXml("CRVSI", ClaimAccountingBuilder.PERIOD,
                ClaimAccountingBuilder.PRODUCT, ClaimAccountingBuilder.COMMENT));
    }

    @Test
    void generateXml_sinResultadoDevuelveNulo() throws SQLException {
        mockProcedure();

        assertNull(repository.generateXml("SINIE", ClaimAccountingBuilder.PERIOD,
                ClaimAccountingBuilder.PRODUCT, ClaimAccountingBuilder.COMMENT));
    }

    @Test
    void generateXml_propagaElErrorComoExcepcionDeBase() {
        when(entityManager.unwrap(Session.class)).thenThrow(new IllegalStateException());

        assertThrows(DatabaseException.class, () -> repository.generateXml("SINIE",
                ClaimAccountingBuilder.PERIOD, ClaimAccountingBuilder.PRODUCT, ClaimAccountingBuilder.COMMENT));
    }

    @Test
    void generateEntry_conValoresNulosDevuelveCamposNulos() throws SQLException {
        Object[] row = new Object[27];
        mockProcedure(row);

        List<AccountingEntryRowDto> rows =
                repository.generateEntry(ClaimAccountingBuilder.COMMENT, ClaimAccountingBuilder.PRODUCT);

        assertNull(rows.get(0).getJournalType());
        assertNull(rows.get(0).getTransactionAmount());
    }

    @Test
    void deleteFiles_ejecutaElBorradoPorProductoYPeriodo() {
        mockNativeQuery(null, null);

        repository.deleteFiles(ClaimAccountingBuilder.PRODUCT, ClaimAccountingBuilder.PERIOD);

        verify(query).executeUpdate();
    }

    @Test
    void saveFile_ejecutaLaInsercion() {
        mockNativeQuery(null, null);

        repository.saveFile(ClaimAccountingBuilder.PRODUCT, "SINIE", ClaimAccountingBuilder.PERIOD,
                ClaimAccountingBuilder.FILE_NAME, ClaimAccountingBuilder.XML_CONTENT,
                ClaimAccountingBuilder.USER);

        verify(query).executeUpdate();
    }

    @Test
    void findFiles_mapeaLasCincoColumnas() {
        mockNativeQuery(null, Collections.singletonList(ClaimAccountingBuilder.fileRow()));

        List<AccountingFileDto> files = repository.findFiles(ClaimAccountingBuilder.PERIOD);

        assertEquals(1, files.size());
        assertEquals(1, files.get(0).getId());
        assertEquals(ClaimAccountingBuilder.PRODUCT, files.get(0).getProduct());
        assertEquals("SINIE", files.get(0).getJournalType());
        assertEquals(ClaimAccountingBuilder.FILE_NAME, files.get(0).getFileName());
        assertEquals("02/09/2026 03:04:45", files.get(0).getGenerationDate());
    }

    @Test
    void findFiles_sinArchivosDevuelveListaVacia() {
        mockNativeQuery(null, Collections.emptyList());

        assertTrue(repository.findFiles(ClaimAccountingBuilder.PERIOD).isEmpty());
    }

    @Test
    void findFiles_conFechaNulaDevuelveCampoNulo() {
        mockNativeQuery(null, Collections.singletonList(
                new Object[] { 1, ClaimAccountingBuilder.PRODUCT, "SINIE",
                        ClaimAccountingBuilder.FILE_NAME, null }));

        assertNull(repository.findFiles(ClaimAccountingBuilder.PERIOD).get(0).getGenerationDate());
    }

    @Test
    void findFile_devuelveNombreYContenido() {
        mockNativeQuery(null, Collections.singletonList(
                new Object[] { ClaimAccountingBuilder.FILE_NAME, ClaimAccountingBuilder.XML_CONTENT }));

        DownloadFileDto file = repository.findFile(1);

        assertEquals(ClaimAccountingBuilder.FILE_NAME, file.getFileName());
        assertEquals(ClaimAccountingBuilder.XML_CONTENT, file.getContent());
    }

    @Test
    void findFile_sinResultadoDevuelveNulo() {
        mockNativeQuery(null, Collections.emptyList());

        assertNull(repository.findFile(99));
    }
}
