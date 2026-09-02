import static org.junit.jupiter.api.Assertions.assertThrows;

import java.util.Date;

import co.com.bnpparibas.cardif.cierres.domain.dtos.AccountingFileDto;
import co.com.bnpparibas.cardif.cierres.domain.dtos.DownloadFileDto;
import co.com.bnpparibas.cardif.cierres.domain.util.exception.RecordNotFoundException;
    
    
    /**
     * El periodo debe llevar el cero antes del mes. Un formato distinto no
     * produce error, devuelve un XML vacio.
     */
    @Test
    void sendEntry_construyeElPeriodoConElCeroAntesDelMes() {
        when(repository.getAccountingPeriodRaw()).thenReturn("2026/02/01");
        when(repository.generateXml(anyString(), anyString(), anyString(), anyString()))
                .thenReturn(ClaimAccountingBuilder.xmlFile("SINIE"));

        service.sendEntry(ClaimAccountingBuilder.sendRequest());

        ArgumentCaptor<String> period = ArgumentCaptor.forClass(String.class);
        verify(repository).generateXml(eq("SINIE"), period.capture(), anyString(), anyString());
        assertEquals("2026/002", period.getValue());
    }

    @Test
    void sendEntry_conMesDeDosDigitosMantieneElCero() {
        when(repository.getAccountingPeriodRaw()).thenReturn("2026/12/31");
        when(repository.generateXml(anyString(), anyString(), anyString(), anyString()))
                .thenReturn(ClaimAccountingBuilder.xmlFile("SINIE"));

        service.sendEntry(ClaimAccountingBuilder.sendRequest());

        ArgumentCaptor<String> period = ArgumentCaptor.forClass(String.class);
        verify(repository).generateXml(eq("SINIE"), period.capture(), anyString(), anyString());
        assertEquals("2026/012", period.getValue());
    }

    @Test
    void sendEntry_generaLosTresTiposDeDiarioYPersisteLosArchivos() {
        when(repository.getAccountingPeriodRaw()).thenReturn("2026/02/01");
        when(repository.generateXml(eq("SINIE"), anyString(), anyString(), anyString()))
                .thenReturn(ClaimAccountingBuilder.xmlFile("SINIE"));
        when(repository.generateXml(eq("LRVSI"), anyString(), anyString(), anyString()))
                .thenReturn(ClaimAccountingBuilder.xmlFile("LRVSI"));
        when(repository.generateXml(eq("CRVSI"), anyString(), anyString(), anyString()))
                .thenReturn(ClaimAccountingBuilder.xmlFile("CRVSI"));

        SendResponseDto response = service.sendEntry(ClaimAccountingBuilder.sendRequest());

        assertEquals(3, response.getFiles().size());
        assertEquals("Interfaz generada correctamente.", response.getMessage());
        verify(repository).deleteFiles(ClaimAccountingBuilder.PRODUCT, "2026/002");
        verify(repository, times(3)).saveFile(anyString(), anyString(), anyString(),
                anyString(), anyString(), anyString());
        verify(repository).markXmlGenerated(ClaimAccountingBuilder.COMMENT, ClaimAccountingBuilder.PRODUCT);
    }

    @Test
    void sendEntry_omiteLosTiposSinAsientos() {
        when(repository.getAccountingPeriodRaw()).thenReturn("2026/02/01");
        when(repository.generateXml(eq("SINIE"), anyString(), anyString(), anyString()))
                .thenReturn(ClaimAccountingBuilder.xmlFile("SINIE"));
        when(repository.generateXml(eq("LRVSI"), anyString(), anyString(), anyString()))
                .thenReturn(null);
        when(repository.generateXml(eq("CRVSI"), anyString(), anyString(), anyString()))
                .thenReturn(null);

        SendResponseDto response = service.sendEntry(ClaimAccountingBuilder.sendRequest());

        assertEquals(1, response.getFiles().size());
        assertTrue(response.getFiles().get(0).contains("SINIE"));
        verify(repository, times(1)).saveFile(anyString(), anyString(), anyString(),
                anyString(), anyString(), anyString());
    }

    @Test
    void sendEntry_sinAsientosNoBorraNiPersisteNiActualizaElEstado() {
        when(repository.getAccountingPeriodRaw()).thenReturn("2026/02/01");
        when(repository.generateXml(anyString(), anyString(), anyString(), anyString()))
                .thenReturn(null);

        SendResponseDto response = service.sendEntry(ClaimAccountingBuilder.sendRequest());

        assertTrue(response.getFiles().isEmpty());
        assertEquals("No se generaron asientos para el producto seleccionado.", response.getMessage());
        verify(repository, never()).deleteFiles(anyString(), anyString());
        verify(repository, never()).saveFile(anyString(), anyString(), anyString(),
                anyString(), anyString(), anyString());
        verify(repository, never()).markXmlGenerated(anyString(), anyString());
    }

    @Test
    void sendEntry_persisteElUsuarioDeLaPeticion() {
        when(repository.getAccountingPeriodRaw()).thenReturn("2026/02/01");
        when(repository.generateXml(eq("SINIE"), anyString(), anyString(), anyString()))
                .thenReturn(ClaimAccountingBuilder.xmlFile("SINIE"));
        when(repository.generateXml(eq("LRVSI"), anyString(), anyString(), anyString()))
                .thenReturn(null);
        when(repository.generateXml(eq("CRVSI"), anyString(), anyString(), anyString()))
                .thenReturn(null);

        service.sendEntry(ClaimAccountingBuilder.sendRequest());

        verify(repository).saveFile(ClaimAccountingBuilder.PRODUCT, "SINIE", "2026/002",
                "SINIE_2012.XML", ClaimAccountingBuilder.XML_CONTENT, ClaimAccountingBuilder.USER);
    }

    @Test
    void getFiles_consultaConElPeriodoContableActual() {
        when(repository.getAccountingPeriodRaw()).thenReturn("2026/02/01");
        when(repository.findFiles(anyString())).thenReturn(
                Collections.singletonList(new AccountingFileDto(1, ClaimAccountingBuilder.PRODUCT,
                        "SINIE", ClaimAccountingBuilder.FILE_NAME, new Date())));

        List<AccountingFileDto> files = service.getFiles();

        assertEquals(1, files.size());
        verify(repository).findFiles("2026/002");
    }

    @Test
    void getFiles_sinArchivosDevuelveListaVacia() {
        when(repository.getAccountingPeriodRaw()).thenReturn("2026/02/01");
        when(repository.findFiles(anyString())).thenReturn(Collections.emptyList());

        assertTrue(service.getFiles().isEmpty());
    }

    @Test
    void downloadFile_devuelveElArchivo() {
        when(repository.findFile(1)).thenReturn(
                new DownloadFileDto(ClaimAccountingBuilder.FILE_NAME, ClaimAccountingBuilder.XML_CONTENT));

        DownloadFileDto file = service.downloadFile(1);

        assertEquals(ClaimAccountingBuilder.FILE_NAME, file.getFileName());
        assertEquals(ClaimAccountingBuilder.XML_CONTENT, file.getContent());
    }

    @Test
    void downloadFile_conArchivoInexistenteLanzaExcepcion() {
        when(repository.findFile(99)).thenReturn(null);

        assertThrows(RecordNotFoundException.class, () -> service.downloadFile(99));
    }
