package co.com.bnpparibas.cardif.closingclaims.domain.services.impl;

import co.com.bnpparibas.cardif.closingclaims.domain.entity.CardifCenterClosing;
import co.com.bnpparibas.cardif.closingclaims.domain.services.ICardifCenterClosingService;
import co.com.bnpparibas.cardif.closingclaims.domain.util.exception.BusinessException;
import co.com.bnpparibas.cardif.closingclaims.domain.util.helpers.CardifCenterClosingExcelHelper;
import co.com.bnpparibas.cardif.closingclaims.domain.util.messages.CardifCenterClosingMessage;
import co.com.bnpparibas.cardif.closingclaims.infraestructure.repository.CardifCenterClosingRepository;
import lombok.extern.slf4j.Slf4j;
import org.springframework.dao.DataAccessException;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.io.IOException;
import java.util.List;

/**
 * Implementación del servicio de cierre de movimientos Cardif Centroamérica.
 */
@Slf4j
@Service
public class CardifCenterClosingServiceImpl
        implements ICardifCenterClosingService {

    private final CardifCenterClosingRepository repository;
    private final CardifCenterClosingExcelHelper excelHelper;

    public CardifCenterClosingServiceImpl(
            CardifCenterClosingRepository repository,
            CardifCenterClosingExcelHelper excelHelper) {
        this.repository = repository;
        this.excelHelper = excelHelper;
    }

    @Override
    @Transactional
    public String generateAccountingEntries(
            String pHeader,
            String correlationId,
            String requestId) {

        long pending = countPending(correlationId, requestId);

        if (pending == 0) {
            return CardifCenterClosingMessage
                    .NO_PENDING_MOVEMENTS.getMessage();
        }

        executeProcedure(correlationId, requestId);
        return CardifCenterClosingMessage
                .ACCOUNTING_ENTRIES_GENERATED.getMessage();
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

    private void executeProcedure(
            String correlationId,
            String requestId) {
        try {
            repository.executeAccountingProcedure();
        } catch (DataAccessException exception) {
            logDatabaseError(
                    "Error ejecutando la contabilización",
                    correlationId,
                    requestId,
                    exception);
            throw databaseException(exception);
        }
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
