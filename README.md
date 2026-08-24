package co.com.bnpparibas.cardif.closingclaims.domain.services.impl;

import co.com.bnpparibas.cardif.closingclaims.domain.dtos.cardifcenterclosing.AccountingXmlFileDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.cardifcenterclosing.AccountingXmlLine;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.cardifcenterclosing.CenterAccountingResultDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.entity.CardifCenterClosing;
import co.com.bnpparibas.cardif.closingclaims.domain.services.ICardifCenterClosingService;
import co.com.bnpparibas.cardif.closingclaims.domain.util.exception.BusinessException;
import co.com.bnpparibas.cardif.closingclaims.domain.util.helpers.CardifCenterAccountingXmlHelper;
import co.com.bnpparibas.cardif.closingclaims.domain.util.helpers.CardifCenterClosingExcelHelper;
import co.com.bnpparibas.cardif.closingclaims.domain.util.messages.CardifCenterClosingMessage;
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
import java.util.Collections;
import java.util.List;

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
    private static final String NO_PENDING_MESSAGE =
            "No hay movimientos para contabilizar.";

    private static final String PROCESSED_STATUS = "PROCESADO";
    private static final String PENDING_STATUS = "SIN MOVIMIENTOS";

    private static final DateTimeFormatter PROCESS_DATE_FORMAT =
            DateTimeFormatter.ofPattern("dd/MM/yyyy hh:mm:ss a");

    private final CardifCenterClosingRepository repository;
    private final CardifCenterClosingExcelHelper excelHelper;
    private final CardifCenterAccountingXmlHelper xmlHelper;
    private final StoredProcedureExecutor storedProcedureExecutor;

    public CardifCenterClosingServiceImpl(
            CardifCenterClosingRepository repository,
            CardifCenterClosingExcelHelper excelHelper,
            CardifCenterAccountingXmlHelper xmlHelper,
            StoredProcedureExecutor storedProcedureExecutor) {
        this.repository = repository;
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

        if (countPending(correlationId, requestId) == 0) {
            return buildResult(
                    NO_PENDING_MESSAGE,
                    PENDING_STATUS,
                    null,
                    Collections.emptyList());
        }

        List<AccountingXmlLine> lines =
                executeProcedure(correlationId, requestId);

        List<AccountingXmlFileDTO> files = buildFiles(
                lines, correlationId, requestId);

        if (files.isEmpty()) {
            throw new BusinessException(
                    null,
                    CardifCenterClosingMessage
                            .NO_ACCOUNTING_ENTRIES_GENERATED.getMessage(),
                    HttpStatus.NOT_FOUND);
        }

        return buildResult(
                SUCCESS_MESSAGE,
                PROCESSED_STATUS,
                lines.get(0).getPeriod(),
                files);
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

    private long countPending(
            String correlationId,
            String requestId) {
        try {
            return repository.countPendingMovements();
        } catch (DataAccessException exception) {
            logDatabaseError(
                    "Error consultando movimientos pendientes",
                    correlationId,
                    requestId,
                    exception);
            throw databaseException(exception);
        }
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

    private List<AccountingXmlFileDTO> buildFiles(
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

    private CenterAccountingResultDTO buildResult(
            String message,
            String status,
            String period,
            List<AccountingXmlFileDTO> files) {

        return CenterAccountingResultDTO.builder()
                .message(message)
                .status(status)
                .period(period)
                .processDate(LocalDateTime.now().format(PROCESS_DATE_FORMAT))
                .files(files)
                .build();
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
