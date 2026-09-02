package co.com.bnpparibas.cardif.controller.impl;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import java.util.Collections;
import java.util.Date;
import java.util.List;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.HttpHeaders;
import org.springframework.http.ResponseEntity;

import co.com.bnpparibas.cardif.builders.ClaimAccountingBuilder;
import co.com.bnpparibas.cardif.cierres.api.controller.impl.ClaimAccountingControllerImpl;
import co.com.bnpparibas.cardif.cierres.domain.dtos.AccountTotalRowDto;
import co.com.bnpparibas.cardif.cierres.domain.dtos.AccountingDateResponseDto;
import co.com.bnpparibas.cardif.cierres.domain.dtos.AccountingEntryRowDto;
import co.com.bnpparibas.cardif.cierres.domain.dtos.AccountingFileDto;
import co.com.bnpparibas.cardif.cierres.domain.dtos.DownloadFileDto;
import co.com.bnpparibas.cardif.cierres.domain.dtos.LoadMessageResponseDto;
import co.com.bnpparibas.cardif.cierres.domain.dtos.ProductResponseDto;
import co.com.bnpparibas.cardif.cierres.domain.dtos.SendResponseDto;
import co.com.bnpparibas.cardif.cierres.domain.service.ClaimAccountingService;
import co.com.bnpparibas.webservicemask.model.ws.response.BNPResponse;

@ExtendWith(MockitoExtension.class)
class ClaimAccountingControllerImplTest {

    @InjectMocks
    private ClaimAccountingControllerImpl controller;

    @Mock
    private ClaimAccountingService service;

    @Test
    void getAccountingDate_devuelveLaFechaEnElCuerpo() {
        when(service.getAccountingDate()).thenReturn(new AccountingDateResponseDto("20260201"));

        BNPResponse response = controller.getAccountingDate();
        AccountingDateResponseDto body = (AccountingDateResponseDto) response.getBodyResponse();

        assertEquals(200, response.getReturnCode());
        assertEquals("20260201", body.getAccountingDate());
    }

    @Test
    @SuppressWarnings("unchecked")
    void getProducts_devuelveLaListaEnElCuerpo() {
        when(service.getProducts()).thenReturn(Arrays.asList(
                new ProductResponseDto("2012"), new ProductResponseDto("2028")));

        BNPResponse response = controller.getProducts();
        List<ProductResponseDto> body = (List<ProductResponseDto>) response.getBodyResponse();

        assertEquals(200, response.getReturnCode());
        assertEquals(2, body.size());
    }

    @Test
    void loadClaims_devuelveElMensajeEnElCuerpo() {
        when(service.loadClaims(any())).thenReturn(new LoadMessageResponseDto("119 Registros Cargados"));

        BNPResponse response = controller.loadClaims(ClaimAccountingBuilder.loadRequest());
        LoadMessageResponseDto body = (LoadMessageResponseDto) response.getBodyResponse();

        assertEquals(200, response.getReturnCode());
        assertEquals("119 Registros Cargados", body.getMessage());
    }

    @Test
    @SuppressWarnings("unchecked")
    void generateEntry_devuelveElDetalleEnElCuerpo() {
        when(service.generateEntry(any())).thenReturn(
                Collections.singletonList(AccountingEntryRowDto.builder().journalType("SINIE").build()));

        BNPResponse response = controller.generateEntry(ClaimAccountingBuilder.generateRequest());
        List<AccountingEntryRowDto> body = (List<AccountingEntryRowDto>) response.getBodyResponse();

        assertEquals(200, response.getReturnCode());
        assertEquals("SINIE", body.get(0).getJournalType());
    }

    @Test
    @SuppressWarnings("unchecked")
    void totalByAccount_devuelveElResumenEnElCuerpo() {
        when(service.totalByAccount(any())).thenReturn(
                Collections.singletonList(AccountTotalRowDto.builder().product("2012").build()));

        BNPResponse response = controller.totalByAccount(ClaimAccountingBuilder.generateRequest());
        List<AccountTotalRowDto> body = (List<AccountTotalRowDto>) response.getBodyResponse();

        assertEquals(200, response.getReturnCode());
        assertEquals("2012", body.get(0).getProduct());
    }

    @Test
    void registerEntry_delegaEnElServicioYNoDevuelveCuerpo() {
        BNPResponse response = controller.registerEntry(ClaimAccountingBuilder.registerRequest());

        verify(service).registerEntry(any());
        assertEquals(200, response.getReturnCode());
        assertNull(response.getBodyResponse());
    }

    @Test
    void sendEntry_devuelveLosArchivosGenerados() {
        when(service.sendEntry(any())).thenReturn(
                new SendResponseDto(Arrays.asList("a.XML", "b.XML"), "Interfaz generada correctamente."));

        BNPResponse response = controller.sendEntry(ClaimAccountingBuilder.sendRequest());
        SendResponseDto body = (SendResponseDto) response.getBodyResponse();

        assertEquals(200, response.getReturnCode());
        assertEquals(2, body.getFiles().size());
        assertNotNull(body.getMessage());
    }

    @Test
    @SuppressWarnings("unchecked")
    void getFiles_devuelveLaListaEnElCuerpo() {
        when(service.getFiles()).thenReturn(Collections.singletonList(
                new AccountingFileDto(1, "2012", "SINIE", "archivo.XML", new Date())));

        BNPResponse response = controller.getFiles();
        List<AccountingFileDto> body = (List<AccountingFileDto>) response.getBodyResponse();

        assertEquals(200, response.getReturnCode());
        assertEquals(1, body.size());
    }

    @Test
    void downloadFile_devuelveElContenidoConElNombreEnLaCabecera() {
        when(service.downloadFile(1)).thenReturn(new DownloadFileDto("archivo.XML", "<SSC/>"));

        ResponseEntity<byte[]> response = controller.downloadFile(1);

        assertEquals(200, response.getStatusCodeValue());
        assertEquals("<SSC/>", new String(response.getBody(), StandardCharsets.UTF_8));
        assertTrue(response.getHeaders().getFirst(HttpHeaders.CONTENT_DISPOSITION).contains("archivo.XML"));
    }

    @Test
    void ping_respondeCorrectamente() {
        BNPResponse response = controller.ping();

        assertEquals(200, response.getReturnCode());
        assertEquals("OK", response.getBodyResponse());
    }
}
