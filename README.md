package co.com.bnpparibas.cardif.service.impl;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyList;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import co.com.bnpparibas.cardif.builders.ClaimAccountingBuilder;
import co.com.bnpparibas.cardif.cierres.domain.dtos.AccountTotalRowDto;
import co.com.bnpparibas.cardif.cierres.domain.dtos.AccountingEntryRowDto;
import co.com.bnpparibas.cardif.cierres.domain.dtos.AccountingFileDto;
import co.com.bnpparibas.cardif.cierres.domain.dtos.DownloadFileDto;
import co.com.bnpparibas.cardif.cierres.domain.dtos.LoadResultDto;
import co.com.bnpparibas.cardif.cierres.domain.dtos.ProductResponseDto;
import co.com.bnpparibas.cardif.cierres.domain.dtos.SendResponseDto;
import co.com.bnpparibas.cardif.cierres.domain.service.impl.ClaimAccountingServiceImpl;
import co.com.bnpparibas.cardif.cierres.domain.util.exception.DataException;
import co.com.bnpparibas.cardif.cierres.domain.util.exception.RecordNotFoundException;
import co.com.bnpparibas.cardif.cierres.domain.util.helpers.ClaimFileHelper;
import co.com.bnpparibas.cardif.cierres.infraestructure.repository.ClaimAccountingRepository;

@ExtendWith(MockitoExtension.class)
class ClaimAccountingServiceImplTest {

    @InjectMocks
    private ClaimAccountingServiceImpl service;

    @Mock
    private ClaimAccountingRepository repository;

    @Mock
    private ClaimFileHelper fileHelper;

    private List<String[]> rows(int total) {
        List<String[]> rows = new ArrayList<>();

        for (int i = 0; i < total; i++) {
            rows.add(new String[ClaimFileHelper.COLUMNS]);
        }

        return rows;
    }

    @Test
    void getAccountingDate_devuelveLaFechaDelRepositorio() {
        when(repository.getAccountingDate()).thenReturn("20260201");

        assertEquals("20260201", service.getAccountingDate().getAccountingDate());
    }

    @Test
    void getProducts_convierteCadaValorEnUnObjetoDeRespuesta() {
        when(repository.getProducts()).thenReturn(Arrays.asList("2012", "2028"));

        List<ProductResponseDto> products = service.getProducts();

        assertEquals(2, products.size());
        assertEquals("2012", products.get(0).getProduct());
        assertEquals("2028", products.get(1).getProduct());
    }

    @Test
    void getProducts_sinProductosDevuelveListaVacia() {
        when(repository.getProducts()).thenReturn(Collections.emptyList());

        assertTrue(service.getProducts().isEmpty());
    }

    @Test
    void loadClaims_limpiaInsertaYEjecutaElProcedimiento() {
        when(repository.findPattern(anyString())).thenReturn(ClaimAccountingBuilder.PATTERN);
        when(fileHelper.read(any())).thenReturn(rows(5));
        when(fileHelper.countIncomplete(anyList())).thenReturn(1);
        when(repository.loadClaims(anyString(), anyString())).thenReturn("5 Registros Cargados");

        LoadResultDto result = service.loadClaims(
                ClaimAccountingBuilder.csvFile("contenido"),
                ClaimAccountingBuilder.PRODUCT,
                ClaimAccountingBuilder.USER);

        assertEquals("5 Registros Cargados", result.getMessage());
        assertEquals(5, result.getTotalRows());
        assertEquals(1, result.getIncompleteRows());
        verify(repository).clearTempClaims();
        verify(repository).insertTempClaims(anyList());
        verify(repository).loadClaims(ClaimAccountingBuilder.PRODUCT, ClaimAccountingBuilder.CSV_NAME);
    }

    @Test
    void loadClaims_sinArchivoLanzaExcepcion() {
        assertThrows(DataException.class,
                () -> service.loadClaims(null, ClaimAccountingBuilder.PRODUCT, ClaimAccountingBuilder.USER));

        verify(repository, never()).clearTempClaims();
    }

    @Test
    void loadClaims_conArchivoVacioLanzaExcepcion() {
        assertThrows(DataException.class, () -> service.loadClaims(
                ClaimAccountingBuilder.csvFile(""),
                ClaimAccountingBuilder.PRODUCT,
                ClaimAccountingBuilder.USER));
    }

    @Test
    void loadClaims_conExtensionInvalidaLanzaExcepcion() {
        assertThrows(DataException.class, () -> service.loadClaims(
                ClaimAccountingBuilder.csvFile("archivo.xlsx", "contenido"),
                ClaimAccountingBuilder.PRODUCT,
                ClaimAccountingBuilder.USER));
    }

    @Test
    void loadClaims_aceptaLaExtensionEnMayusculas() {
        when(repository.findPattern(anyString())).thenReturn(ClaimAccountingBuilder.PATTERN);
        when(fileHelper.read(any())).thenReturn(rows(1));
        when(repository.loadClaims(anyString(), anyString())).thenReturn("1 Registros Cargados");

        LoadResultDto result = service.loadClaims(
                ClaimAccountingBuilder.csvFile("326CO21SR0122026090110.CSV", "contenido"),
                ClaimAccountingBuilder.PRODUCT,
                ClaimAccountingBuilder.USER);

        assertEquals(1, result.getTotalRows());
    }

    @Test
    void loadClaims_conProductoSinPatronLanzaExcepcion() {
        when(repository.findPattern(anyString())).thenReturn(null);

        assertThrows(DataException.class, () -> service.loadClaims(
                ClaimAccountingBuilder.csvFile("contenido"),
                ClaimAccountingBuilder.PRODUCT,
                ClaimAccountingBuilder.USER));

        verify(repository, never()).clearTempClaims();
    }

    @Test
    void loadClaims_conPatronVacioLanzaExcepcion() {
        when(repository.findPattern(anyString())).thenReturn("   ");

        assertThrows(DataException.class, () -> service.loadClaims(
                ClaimAccountingBuilder.csvFile("contenido"),
                ClaimAccountingBuilder.PRODUCT,
                ClaimAccountingBuilder.USER));
    }

    @Test
    void loadClaims_conArchivoDeOtroProductoLanzaExcepcion() {
        when(repository.findPattern(anyString())).thenReturn(ClaimAccountingBuilder.PATTERN);

        assertThrows(DataException.class, () -> service.loadClaims(
                ClaimAccountingBuilder.csvFile("326CO21SR0272026090110.csv", "contenido"),
                ClaimAccountingBuilder.PRODUCT,
                ClaimAccountingBuilder.USER));

        verify(repository, never()).clearTempClaims();
    }

    @Test
    void generateEntry_delegaEnElRepositorio() {
        List<AccountingEntryRowDto> expected =
                Collections.singletonList(AccountingEntryRowDto.builder().journalType("SINIE").build());
        when(repository.generateEntry(anyString(), anyString())).thenReturn(expected);

        List<AccountingEntryRowDto> rows = service.generateEntry(ClaimAccountingBuilder.generateRequest());

        assertEquals(1, rows.size());
        verify(repository).generateEntry(ClaimAccountingBuilder.COMMENT, ClaimAccountingBuilder.PRODUCT);
    }

    @Test
    void totalByAccount_delegaEnElRepositorio() {
        List<AccountTotalRowDto> expected =
                Collections.singletonList(AccountTotalRowDto.builder().product("2012").build());
        when(repository.totalByAccount(anyString(), anyString())).thenReturn(expected);

        List<AccountTotalRowDto> rows = service.totalByAccount(ClaimAccountingBuilder.generateRequest());

        assertEquals(1, rows.size());
        verify(repository).totalByAccount(ClaimAccountingBuilder.COMMENT, ClaimAccountingBuilder.PRODUCT);
    }

    @Test
    void registerEntry_delegaEnElRepositorio() {
        service.registerEntry(ClaimAccountingBuilder.registerRequest());

        verify(repository).registerEntry(ClaimAccountingBuilder.COMMENT, ClaimAccountingBuilder.PRODUCT);
    }

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
                        "SINIE", ClaimAccountingBuilder.FILE_NAME, "02/09/2026 03:04:45")));

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
}
