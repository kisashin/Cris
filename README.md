import org.springframework.web.multipart.MultipartFile;

import co.com.bnpparibas.cardif.cierres.domain.dtos.LoadResultDto;
import co.com.bnpparibas.cardif.cierres.domain.util.constants.ExceptionConstants;
import co.com.bnpparibas.cardif.cierres.domain.util.exception.DataException;
import co.com.bnpparibas.cardif.cierres.domain.util.helpers.ClaimFileHelper;
    
    
    
    private final ClaimAccountingRepository repository;
    private final ClaimFileHelper fileHelper;

    private static final String CSV_EXTENSION = ".csv";



    @Override
    @Transactional(transactionManager = "transactionManager", rollbackFor = Exception.class)
    public LoadResultDto loadClaims(MultipartFile file, String product, String user) {
        String fileName = validate(file, product);

        List<String[]> rows = fileHelper.read(file);
        int incomplete = fileHelper.countIncomplete(rows);

        repository.clearTempClaims();
        repository.insertTempClaims(rows);

        String message = repository.loadClaims(product, fileName);

        log.info("Carga finalizada producto {} archivo {} filas {} incompletas {} usuario {}",
                product, fileName, rows.size(), incomplete, user);

        return new LoadResultDto(message, rows.size(), incomplete);
    }

    /**
     * Replica el filtro por patron que el procedimiento hacia sobre el nombre de
     * los archivos de la carpeta de entrada.
     */
    protected String validate(MultipartFile file, String product) {
        if (file == null || file.isEmpty()) {
            throw new DataException(ExceptionConstants.FILE_REQUIRED);
        }

        String fileName = file.getOriginalFilename();

        if (fileName == null || !fileName.toLowerCase().endsWith(CSV_EXTENSION)) {
            throw new DataException(ExceptionConstants.FILE_EXTENSION);
        }

        String pattern = repository.findPattern(product);

        if (pattern == null || pattern.trim().isEmpty()) {
            throw new DataException(ExceptionConstants.PRODUCT_WITHOUT_PATTERN);
        }

        if (!fileName.toUpperCase().startsWith(pattern.trim().toUpperCase())) {
            throw new DataException(ExceptionConstants.FILE_PATTERN + pattern.trim());
        }

        return fileName;
    }    
    
