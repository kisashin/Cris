package co.com.bnpparibas.cardif.service.impl;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

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
import co.com.bnpparibas.cardif.cierres.domain.dtos.LoadMessageResponseDto;
import co.com.bnpparibas.cardif.cierres.domain.dtos.ProductResponseDto;
import co.com.bnpparibas.cardif.cierres.domain.dtos.SendResponseDto;
import co.com.bnpparibas.cardif.cierres.domain.service.impl.ClaimAccountingServiceImpl;
import co.com.bnpparibas.cardif.cierres.infraestructure.repository.ClaimAccountingRepository;

@ExtendWith(MockitoExtension.class)
class ClaimAccountingServiceImplTest {

    @InjectMocks
    private ClaimAccountingServiceImpl service;

    @Mock
    private ClaimAccountingRepository repository;

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
    void loadClaims_conLayoutUnoUsaLaCargaAlterna() {
        when(repository.countProductLayout(anyString())).thenReturn(1);
        when(repository.loadClaims(anyString(), eq(true))).thenReturn("119 Registros Cargados");

        LoadMessageResponseDto response = service.loadClaims(ClaimAccountingBuilder.loadRequest());

        assertEquals("119 Registros Cargados", response.getMessage());
        verify(repository).loadClaims(ClaimAccountingBuilder.PRODUCT, true);
    }

    @Test
    void loadClaims_sinLayoutUnoUsaLaCargaEstandar() {
        when(repository.countProductLayout(anyString())).thenReturn(0);
        when(repository.loadClaims(anyString(), eq(false))).thenReturn("No hay archivo de siniestros");

        LoadMessageResponseDto response = service.loadClaims(ClaimAccountingBuilder.loadRequest());

        assertEquals("No hay archivo de siniestros", response.getMessage());
        verify(repository).loadClaims(ClaimAccountingBuilder.PRODUCT, false);
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
        when(repository.generateXml(anyString(), anyString(), anyString(), anyString())).thenReturn("<SSC/>");

        service.sendEntry(ClaimAccountingBuilder.sendRequest());

        ArgumentCaptor<String> period = ArgumentCaptor.forClass(String.class);
        verify(repository).generateXml(eq("SINIE"), period.capture(), anyString(), anyString());
        assertEquals("2026/002", period.getValue());
    }

    @Test
    void sendEntry_conMesDeDosDigitosMantieneElCero() {
        when(repository.getAccountingPeriodRaw()).thenReturn("2026/12/31");
        when(repository.generateXml(anyString(), anyString(), anyString(), anyString())).thenReturn("<SSC/>");

        service.sendEntry(ClaimAccountingBuilder.sendRequest());

        ArgumentCaptor<String> period = ArgumentCaptor.forClass(String.class);
        verify(repository).generateXml(eq("SINIE"), period.capture(), anyString(), anyString());
        assertEquals("2026/012", period.getValue());
    }

    @Test
    void sendEntry_generaLosTresTiposDeDiarioYActualizaElEstado() {
        when(repository.getAccountingPeriodRaw()).thenReturn("2026/02/01");
        when(repository.generateXml(anyString(), anyString(), anyString(), anyString())).thenReturn("<SSC/>");

        SendResponseDto response = service.sendEntry(ClaimAccountingBuilder.sendRequest());

        assertEquals(3, response.getFiles().size());
        assertEquals("Interfaz enviada a contabilidad.", response.getMessage());
        verify(repository, times(3)).generateXml(anyString(), anyString(), anyString(), anyString());
        verify(repository).markXmlGenerated(ClaimAccountingBuilder.COMMENT, ClaimAccountingBuilder.PRODUCT);
    }

    @Test
    void sendEntry_omiteLosTiposSinAsientos() {
        when(repository.getAccountingPeriodRaw()).thenReturn("2026/02/01");
        when(repository.generateXml(eq("SINIE"), anyString(), anyString(), anyString())).thenReturn("<SSC/>");
        when(repository.generateXml(eq("LRVSI"), anyString(), anyString(), anyString())).thenReturn("");
        when(repository.generateXml(eq("CRVSI"), anyString(), anyString(), anyString())).thenReturn(null);

        SendResponseDto response = service.sendEntry(ClaimAccountingBuilder.sendRequest());

        assertEquals(1, response.getFiles().size());
        assertTrue(response.getFiles().get(0).contains("SINIE"));
    }

    @Test
    void sendEntry_sinAsientosNoActualizaElEstado() {
        when(repository.getAccountingPeriodRaw()).thenReturn("2026/02/01");
        when(repository.generateXml(anyString(), anyString(), anyString(), anyString())).thenReturn("");

        SendResponseDto response = service.sendEntry(ClaimAccountingBuilder.sendRequest());

        assertTrue(response.getFiles().isEmpty());
        assertEquals("No se generaron asientos para enviar.", response.getMessage());
        verify(repository, never()).markXmlGenerated(anyString(), anyString());
    }

    @Test
    void sendEntry_construyeElNombreDelArchivoComoElProcedimiento() {
        when(repository.getAccountingPeriodRaw()).thenReturn("2026/02/01");
        when(repository.generateXml(anyString(), anyString(), anyString(), anyString())).thenReturn("<SSC/>");

        SendResponseDto response = service.sendEntry(ClaimAccountingBuilder.sendRequest());

        assertEquals("2012_202602SINIE_20122026.XML", response.getFiles().get(0));
    }

    @Test
    void buildXmlName_recortaElComentarioYReemplazaLosEspacios() {
        String name = service.buildXmlName("comentario muy largo de prueba", "SINIE", "2012", "2026/002");

        assertTrue(name.startsWith("comentario_muy_largo"));
        assertTrue(name.endsWith(".XML"));
    }

    @Test
    void buildXmlName_quitaElCeroInicialDelProducto() {
        String name = service.buildXmlName("ajuste", "SINIE", "0430", "2026/002");

        assertTrue(name.contains("430"));
    }

    @Test
    void buildXmlName_conValoresNulosNoFalla() {
        String name = service.buildXmlName(null, "SINIE", null, "2026/002");

        assertEquals("SINIE_2026.XML", name);
    }
}
