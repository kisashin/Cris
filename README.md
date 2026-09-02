    @Override
    public BNPResponse loadClaims(MultipartFile file, String product, String user) {
        return new BNPResponse(HttpStatus.OK, HttpStatus.OK.name(),
                service.loadClaims(file, product, user));
    }


import org.springframework.web.multipart.MultipartFile;    
