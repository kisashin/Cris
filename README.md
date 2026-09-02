    @Override
    public BNPResponse getFiles() {
        return new BNPResponse(HttpStatus.OK, HttpStatus.OK.name(), service.getFiles());
    }

    @Override
    public ResponseEntity<byte[]> downloadFile(Integer id) {
        DownloadFileDto file = service.downloadFile(id);
        byte[] content = file.getContent().getBytes(StandardCharsets.UTF_8);

        return ResponseEntity.ok()
                .header(HttpHeaders.CONTENT_DISPOSITION,
                        "attachment; filename=\"" + file.getFileName() + "\"")
                .contentType(MediaType.APPLICATION_OCTET_STREAM)
                .body(content);
    }




import java.nio.charset.StandardCharsets;

import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;

import co.com.bnpparibas.cardif.cierres.domain.dtos.DownloadFileDto;
