package co.com.bnpparibas.cardif.closingclaims.domain.services.impl;

import co.com.bnpparibas.cardif.closingclaims.domain.dtos.cardifcenterclosing.AccountingXmlFile;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.cardifcenterclosing.AccountingXmlFileDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.cardifcenterclosing.AccountingXmlLine;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.cardifcenterclosing.CenterAccountingResultDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.entity.ArchivoAsientoCentro;
import co.com.bnpparibas.cardif.closingclaims.domain.entity.CardifCenterClosing;
import co.com.bnpparibas.cardif.closingclaims.domain.services.ICardifCenterClosingService;
import co.com.bnpparibas.cardif.closingclaims.domain.util.exception.BusinessException;
import co.com.bnpparibas.cardif.closingclaims.domain.util.helpers.CardifCenterAccountingXmlHelper;
import co.com.bnpparibas.cardif.closingclaims.domain.util.helpers.CardifCenterClosingExcelHelper;
import co.com.bnpparibas.cardif.closingclaims.domain.util.messages.CardifCenterClosingMessage;
import co.com.bnpparibas.cardif.closingclaims.infraestructure.repository.ArchivoAsientoCentroRepository;
import co.com.bnpparibas.cardif.closingclaims.infraestructure.repository.CardifCenterClosingRepository;
import co.com.bnpparibas.cardif.closingclaims.infraestructure.repository.StoredProcedureExecutor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.dao.DataAccessException;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.io.IOException;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

/**
 * Implementacion del servicio de cierre de movimientos Cardif Centroamerica.
 */
@Slf4j
@Service
public class CardifCenterClosingServiceImpl
        implements ICardifCenterClosingService {

    private static final String PROCEDURE_CALL =
            "EXEC dbo.sp_contabiliza_cardifCentro";

    private static final String SUCCESS_MESSAGE =
            "Asientos generados con éxito.";
    private static final String GENERATED_STATUS = "GENERADO";

    private static final DateTimeFormatter PROCESS_DATE_FORMAT =
            DateTimeFormatter.ofPattern("dd/MM/yyyy hh:mm:ss a");

    private final CardifCenterClosingRepository repository;
    private final ArchivoAsientoCentroRepository fileRepository;
    private final CardifCenterClosingExcelHelper excelHelper;
    private final CardifCenterAccountingXmlHelper xmlHelper;
    private final StoredProcedureExecutor storedProcedureExecutor;

    public CardifCenterClosingServiceImpl(
            CardifCenterClosingRepository repository,
            ArchivoAsientoCentroRepository fileRepository,
            CardifCenterClosingExcelHelper excelHelper,
            CardifCenterAccountingXmlHelper xmlHelper,
            StoredProcedureExecutor storedProcedureExecutor) {
        this.repository = repository;
        this.fileRepository = fileRepository;
        this.excelHelper = excelHelper;
        this.xmlHelper = xmlHelper;
        this.storedProcedureExecutor = storedProcedureExecutor;
    }

    @Override
    @Transactional
    public CenterAccountingResultDTO generateAccountingEntries(
            String pHeader,
            String correlationId,
            String requestId) {

        List<AccountingXmlLine> lines =
                executeProcedure(correlationId, requestId);

        List<AccountingXmlFile> files =
                buildFiles(lines, correlationId, requestId);

        if (files.isEmpty()) {
            throw new BusinessException(
                    null,
                    CardifCenterClosingMessage
                            .NO_ACCOUNTING_ENTRIES_GENERATED.getMessage(),
                    HttpStatus.NOT_FOUND);
        }

        String period = lines.get(0).getPeriod();
        List<ArchivoAsientoCentro> saved =
                saveFiles(files, period, correlationId, requestId);

        return CenterAccountingResultDTO.builder()
                .message(SUCCESS_MESSAGE)
                .period(period)
                .files(toDto(saved))
                .build();
    }

    @Override
    @Transactional(readOnly = true)
    public List<AccountingXmlFileDTO> findGeneratedFiles(
            String correlationId,
            String requestId) {
        try {
            return toDto(fileRepository.findLatest());
        } catch (DataAccessException exception) {
            logDatabaseError(
                    "Error consultando los archivos generados",
                    correlationId,
                    requestId,
                    exception);
            throw databaseException(exception);
        }
    }

    @Override
    @Transactional(readOnly = true)
    public ArchivoAsientoCentro findXmlFile(
            Integer id,
            String correlationId,
            String requestId) {

        ArchivoAsientoCentro file;

        try {
            file = fileRepository.findById(id).orElse(null);
        } catch (DataAccessException exception) {
            logDatabaseError(
                    "Error consultando el archivo XML",
                    correlationId,
                    requestId,
                    exception);
            throw databaseException(exception);
        }

        if (file == null || file.getContenido() == null) {
            throw new BusinessException(
                    null,
                    CardifCenterClosingMessage
                            .XML_FILE_NOT_FOUND.getMessage(),
                    HttpStatus.NOT_FOUND);
        }

        return file;
    }

    @Override
    @Transactional(readOnly = true)
    public byte[] downloadMovementsReport(
            String pHeader,
            String correlationId,
            String requestId) {

        List<CardifCenterClosing> movements =
                findMovements(correlationId, requestId);

        validateMovements(movements);
        return generateExcel(movements, correlationId, requestId);
    }

    private List<AccountingXmlLine> executeProcedure(
            String correlationId,
            String requestId) {
        try {
            return storedProcedureExecutor.query(
                    PROCEDURE_CALL,
                    resultSet -> AccountingXmlLine.builder()
                            .period(resultSet.getString("Periodo"))
                            .pass(resultSet.getInt("Pasada"))
                            .lineType(resultSet.getInt("id"))
                            .movementType(resultSet.getString("Mv"))
                            .sequence(resultSet.getLong("Secuencia"))
                            .content(resultSet.getString("Line"))
                            .build());
        } catch (DataAccessException exception) {
            logDatabaseError(
                    "Error ejecutando la contabilización",
                    correlationId,
                    requestId,
                    exception);
            throw databaseException(exception);
        }
    }

    private List<AccountingXmlFile> buildFiles(
            List<AccountingXmlLine> lines,
            String correlationId,
            String requestId) {
        try {
            return xmlHelper.buildFiles(lines);
        } catch (RuntimeException exception) {
            log.error(
                    "Error generando archivos XML. correlationId={}, requestId={}",
                    correlationId,
                    requestId,
                    exception);
            throw new BusinessException(
                    exception,
                    null,
                    CardifCenterClosingMessage
                            .XML_GENERATION_ERROR.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    private List<ArchivoAsientoCentro> saveFiles(
            List<AccountingXmlFile> files,
            String period,
            String correlationId,
            String requestId) {

        String batchId = UUID.randomUUID().toString();
        LocalDateTime processDate = LocalDateTime.now();
        List<ArchivoAsientoCentro> entities = new ArrayList<>();

        for (AccountingXmlFile file : files) {
            entities.add(ArchivoAsientoCentro.builder()
                    .idLote(batchId)
                    .periodo(period)
                    .tipoMovimiento(file.getMovementType())
                    .nombreArchivo(file.getFileName())
                    .contenido(file.getContent())
                    .cantidadLineas(file.getLineCount())
                    .fechaproceso(processDate)
                    .estado(GENERATED_STATUS)
                    .build());
        }

        try {
            return fileRepository.saveAll(entities);
        } catch (DataAccessException exception) {
            logDatabaseError(
                    "Error guardando los archivos XML",
                    correlationId,
                    requestId,
                    exception);
            throw databaseException(exception);
        }
    }

    private List<AccountingXmlFileDTO> toDto(
            List<ArchivoAsientoCentro> files) {

        return files.stream()
                .map(file -> AccountingXmlFileDTO.builder()
                        .id(file.getId())
                        .period(file.getPeriodo())
                        .movementType(file.getTipoMovimiento())
                        .fileName(file.getNombreArchivo())
                        .lineCount(file.getCantidadLineas())
                        .processDate(file.getFechaproceso() == null
                                ? null
                                : file.getFechaproceso()
                                        .format(PROCESS_DATE_FORMAT))
                        .status(file.getEstado())
                        .build())
                .collect(Collectors.toList());
    }

    private List<CardifCenterClosing> findMovements(
            String correlationId,
            String requestId) {
        try {
            return repository.findAllForExport();
        } catch (DataAccessException exception) {
            logDatabaseError(
                    "Error consultando los movimientos del reporte",
                    correlationId,
                    requestId,
                    exception);
            throw databaseException(exception);
        }
    }

    private byte[] generateExcel(
            List<CardifCenterClosing> movements,
            String correlationId,
            String requestId) {
        try {
            return excelHelper.generateExcel(movements);
        } catch (IOException exception) {
            log.error(
                    "Error generando Excel. correlationId={}, requestId={}",
                    correlationId,
                    requestId,
                    exception);
            throw new BusinessException(
                    exception,
                    null,
                    CardifCenterClosingMessage
                            .EXCEL_GENERATION_ERROR.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    private void validateMovements(
            List<CardifCenterClosing> movements) {
        if (movements == null || movements.isEmpty()) {
            throw new BusinessException(
                    null,
                    CardifCenterClosingMessage
                            .NO_MOVEMENTS_TO_EXPORT.getMessage(),
                    HttpStatus.NOT_FOUND);
        }
    }

    private void logDatabaseError(
            String message,
            String correlationId,
            String requestId,
            DataAccessException exception) {
        log.error(
                "{}. correlationId={}, requestId={}",
                message,
                correlationId,
                requestId,
                exception);
    }

    private BusinessException databaseException(
            DataAccessException exception) {
        return new BusinessException(
                exception,
                null,
                CardifCenterClosingMessage
                        .DATABASE_ACCESS_ERROR.getMessage(),
                HttpStatus.INTERNAL_SERVER_ERROR);
    }
}
