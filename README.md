import static org.mockito.Mockito.verify;

import java.util.Collections;

import co.com.bnpparibas.cardif.cierres.domain.dtos.AccountingFileDto;
import co.com.bnpparibas.cardif.cierres.domain.dtos.DownloadFileDto;
import co.com.bnpparibas.cardif.cierres.domain.dtos.XmlFileDto;
    
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
    }

    @Test
    void findFiles_sinArchivosDevuelveListaVacia() {
        mockNativeQuery(null, Collections.emptyList());

        assertTrue(repository.findFiles(ClaimAccountingBuilder.PERIOD).isEmpty());
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




        private void mockNativeQuery(Object singleResult, List<?> resultList) {
        when(entityManager.createNativeQuery(anyString())).thenReturn(query);
        when(query.setParameter(anyString(), any())).thenReturn(query);
        when(query.getSingleResult()).thenReturn(singleResult);
        when(query.getResultList()).thenReturn(resultList);
        when(query.executeUpdate()).thenReturn(1);
    }
