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




 import static org.junit.jupiter.api.Assertions.assertTrue;

import java.nio.charset.StandardCharsets;
import java.util.Date;

import org.springframework.http.HttpHeaders;
import org.springframework.http.ResponseEntity;

import co.com.bnpparibas.cardif.cierres.domain.dtos.AccountingFileDto;
import co.com.bnpparibas.cardif.cierres.domain.dtos.DownloadFileDto;   
