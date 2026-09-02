    @GetMapping(path = "/files", produces = { "application/json" })
    BNPResponse getFiles();

    @GetMapping(path = "/files/{id}/download")
    ResponseEntity<byte[]> downloadFile(@PathVariable("id") Integer id);

    import org.springframework.http.ResponseEntity;
