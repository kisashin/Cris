import org.springframework.transaction.annotation.Transactional;

import co.com.bnpparibas.cardif.cierres.domain.dtos.AccountingFileDto;
import co.com.bnpparibas.cardif.cierres.domain.dtos.DownloadFileDto;
import co.com.bnpparibas.cardif.cierres.domain.dtos.XmlFileDto;
import co.com.bnpparibas.cardif.cierres.domain.util.exception.RecordNotFoundException;
    
    
    private static final String[] JOURNAL_TYPES = { "SINIE", "LRVSI", "CRVSI" };

    private static final String MESSAGE_SENT = "Interfaz generada correctamente.";
    private static final String MESSAGE_EMPTY = "No se generaron asientos para el producto seleccionado.";
    private static final String MESSAGE_FILE_NOT_FOUND = "El archivo solicitado no existe.";

    private final ClaimAccountingRepository repository;
















        @Override
    @Transactional
    public SendResponseDto sendEntry(SendAccountingRequestDto request) {
        String period = buildPeriod(repository.getAccountingPeriodRaw());
        List<XmlFileDto> generated = new ArrayList<>();

        for (String journalType : JOURNAL_TYPES) {
            XmlFileDto file = repository.generateXml(
                    journalType, period, request.getProduct(), request.getComment());

            if (file != null) {
                generated.add(file);
            }
        }

        if (generated.isEmpty()) {
            return new SendResponseDto(new ArrayList<>(), MESSAGE_EMPTY);
        }

        repository.deleteFiles(request.getProduct(), period);

        List<String> names = new ArrayList<>();

        for (XmlFileDto file : generated) {
            repository.saveFile(request.getProduct(), file.getJournalType(), period,
                    file.getFileName(), file.getContent(), request.getUser());

            names.add(file.getFileName());
        }

        repository.markXmlGenerated(request.getComment(), request.getProduct());

        log.info("Generacion finalizada producto {} archivos {}", request.getProduct(), names.size());

        return new SendResponseDto(names, MESSAGE_SENT);
    }



        @Override
    @Transactional(readOnly = true)
    public List<AccountingFileDto> getFiles() {
        return repository.findFiles(buildPeriod(repository.getAccountingPeriodRaw()));
    }

    @Override
    @Transactional(readOnly = true)
    public DownloadFileDto downloadFile(Integer id) {
        DownloadFileDto file = repository.findFile(id);

        if (file == null) {
            throw new RecordNotFoundException(MESSAGE_FILE_NOT_FOUND);
        }

        return file;
    }
