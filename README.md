    @PostMapping(path = "/load", consumes = { "multipart/form-data" }, produces = { "application/json" })
    BNPResponse loadClaims(@RequestPart("file") MultipartFile file,
                           @RequestPart("product") String product,
                           @RequestPart("user") String user);

import org.springframework.web.multipart.MultipartFile;
                           
