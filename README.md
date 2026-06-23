package co.com.bnpparibas.cardif.closingclaims.domain.services.impl;

import co.com.bnpparibas.cardif.closingclaims.domain.entity.CardifPeruClosing;
import co.com.bnpparibas.cardif.closingclaims.domain.services.ICardifPeruClosingService;
import co.com.bnpparibas.cardif.closingclaims.domain.util.exception.BusinessException;
import co.com.bnpparibas.cardif.closingclaims.domain.util.helpers.CardifPeruClosingExcelHelper;
import co.com.bnpparibas.cardif.closingclaims.infraestructure.repository.CardifPeruClosingRepository;
import lombok.extern.slf4j.Slf4j;
import org.springframework.dao.DataAccessException;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.io.IOException;
import java.util.List;

/**
 * Implementación del servicio de cierre de movimientos Cardif Perú.
 */
@Slf4j
@Service
public class CardifPeruClosingServiceImpl
        implements ICardifPeruClosingService {

    private static final String SUCCESS_MESSAGE =
            "Asientos generados con éxito.";
    private static final String NO_PENDING_MESSAGE =
            "No hay movimientos para contabilizar.";

    private final CardifPeruClosingRepository repository;
    private final CardifPeruClosingExcelHelper excelHelper;

    public CardifPeruClosingServiceImpl(
            CardifPeruClosingRepository repository,
            CardifPeruClosingExcelHelper excelHelper) {
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
            return NO_PENDING_MESSAGE;
        }

        executeProcedure(correlationId, requestId);
        return SUCCESS_MESSAGE;
    }

    @Override
    @Transactional(readOnly = true)
    public byte[] downloadMovementsReport(
            String pHeader,
            String correlationId,
            String requestId) {

        List<CardifPeruClosing> movements =
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

    private List<CardifPeruClosing> findMovements(
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
            List<CardifPeruClosing> movements,
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
                    "Error al generar el archivo Excel",
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    private void validateMovements(
            List<CardifPeruClosing> movements) {
        if (movements == null || movements.isEmpty()) {
            throw new BusinessException(
                    null,
                    "No existen movimientos para generar el archivo",
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
                "Error al acceder a la información del cierre de movimientos",
                HttpStatus.INTERNAL_SERVER_ERROR);
    }
}
