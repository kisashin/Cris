package co.com.bnpparibas.cardif.cierres.domain.service.impl;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.locks.ReentrantLock;
import java.util.stream.Collectors;

import org.springframework.stereotype.Service;

import co.com.bnpparibas.cardif.cierres.api.dtos.GenerateAccountingRequestDto;
import co.com.bnpparibas.cardif.cierres.api.dtos.LoadClaimRequestDto;
import co.com.bnpparibas.cardif.cierres.api.dtos.RegisterAccountingRequestDto;
import co.com.bnpparibas.cardif.cierres.api.dtos.SendAccountingRequestDto;
import co.com.bnpparibas.cardif.cierres.domain.dtos.AccountTotalRowDto;
import co.com.bnpparibas.cardif.cierres.domain.dtos.AccountingDateResponseDto;
import co.com.bnpparibas.cardif.cierres.domain.dtos.AccountingEntryRowDto;
import co.com.bnpparibas.cardif.cierres.domain.dtos.LoadMessageResponseDto;
import co.com.bnpparibas.cardif.cierres.domain.dtos.ProductResponseDto;
import co.com.bnpparibas.cardif.cierres.domain.dtos.SendResponseDto;
import co.com.bnpparibas.cardif.cierres.domain.service.ClaimAccountingService;
import co.com.bnpparibas.cardif.cierres.infraestructure.repository.ClaimAccountingRepository;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Service
@Slf4j
@RequiredArgsConstructor
public class ClaimAccountingServiceImpl implements ClaimAccountingService {

    private static final String[] JOURNAL_TYPES = { "SINIE", "LRVSI", "CRVSI" };

    private static final String MESSAGE_SENT = "Interfaz enviada a contabilidad.";
    private static final String MESSAGE_EMPTY = "No se generaron asientos para enviar.";

    private static final int COMMENT_MAX_LENGTH = 20;
    private static final String XML_EXTENSION = ".XML";

    /**
     * El procedimiento del XML usa tablas temporales globales, por lo que dos
     * envios simultaneos se interfieren entre si.
     */
    private static final ReentrantLock SEND_LOCK = new ReentrantLock();

    private final ClaimAccountingRepository repository;

    @Override
    public AccountingDateResponseDto getAccountingDate() {
        return new AccountingDateResponseDto(repository.getAccountingDate());
    }

    @Override
    public List<ProductResponseDto> getProducts() {
        return repository.getProducts().stream()
                .map(ProductResponseDto::new)
                .collect(Collectors.toList());
    }

    @Override
    public LoadMessageResponseDto loadClaims(LoadClaimRequestDto request) {
        boolean alpha = repository.countProductLayout(request.getProduct()) > 0;
        String message = repository.loadClaims(request.getProduct(), alpha);

        return new LoadMessageResponseDto(message);
    }

    @Override
    public List<AccountingEntryRowDto> generateEntry(GenerateAccountingRequestDto request) {
        return repository.generateEntry(request.getComment(), request.getProduct());
    }

    @Override
    public List<AccountTotalRowDto> totalByAccount(GenerateAccountingRequestDto request) {
        return repository.totalByAccount(request.getComment(), request.getProduct());
    }

    @Override
    public void registerEntry(RegisterAccountingRequestDto request) {
        repository.registerEntry(request.getComment(), request.getProduct());
    }

    @Override
    public SendResponseDto sendEntry(SendAccountingRequestDto request) {
        log.info("Envio solicitado producto {} comentario {} candado ocupado {}",
                request.getProduct(), request.getComment(), SEND_LOCK.isLocked());

        SEND_LOCK.lock();
        long start = System.currentTimeMillis();
        try {
            log.info("Envio iniciado producto {}", request.getProduct());

            String period = buildPeriod(repository.getAccountingPeriodRaw());
            List<String> files = new ArrayList<>();

            for (String journalType : JOURNAL_TYPES) {
                String xml = repository.generateXml(journalType, period, request.getProduct(), request.getComment());

                if (xml == null || xml.isEmpty()) {
                    log.info("Sin asientos para el tipo de diario {}", journalType);
                    continue;
                }

                files.add(buildXmlName(request.getComment(), journalType, request.getProduct(), period));
            }

            if (files.isEmpty()) {
                log.info("Envio sin asientos producto {} duracion {} ms",
                        request.getProduct(), System.currentTimeMillis() - start);
                return new SendResponseDto(files, MESSAGE_EMPTY);
            }

            repository.markXmlGenerated(request.getComment(), request.getProduct());

            log.info("Envio finalizado producto {} archivos {} duracion {} ms",
                    request.getProduct(), files.size(), System.currentTimeMillis() - start);

            return new SendResponseDto(files, MESSAGE_SENT);
        } finally {
            SEND_LOCK.unlock();
        }
    }

    /**
     * Periodo con el formato que espera el procedimiento del XML: el anio, una
     * barra, un cero y el mes. Un formato distinto no produce error, devuelve un
     * XML vacio.
     */
    protected String buildPeriod(String rawPeriod) {
        return rawPeriod.substring(0, 4) + "/0" + rawPeriod.substring(5, 7);
    }

    /**
     * Replica el nombre que arma el procedimiento: comentario recortado, tipo de
     * diario, producto sin el cero inicial y periodo sin la barra.
     */
    protected String buildXmlName(String comment, String journalType, String product, String period) {
        String prefix = comment == null ? "" : comment.trim();

        if (prefix.length() > COMMENT_MAX_LENGTH) {
            prefix = prefix.substring(0, COMMENT_MAX_LENGTH);
        }

        String code = product == null ? "" : product;

        if (code.startsWith("0")) {
            code = code.substring(1);
        }

        String name = prefix + journalType + "_" + code + period.replace("/0", "") + XML_EXTENSION;

        return name.replace(" ", "_");
    }
}
