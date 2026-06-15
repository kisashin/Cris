src/main/java/co/com/bnpparibas/cardif/closingclaims/domain/services/impl/PeruAccountingReportServiceImpl.java

package co.com.bnpparibas.cardif.closingclaims.domain.services.impl;

import co.com.bnpparibas.cardif.closingclaims.domain.dtos.peruaccountingreport.PeruAccountingReportResponseDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.entity.PeruAccountingReport;
import co.com.bnpparibas.cardif.closingclaims.domain.services.IPeruAccountingReportService;
import co.com.bnpparibas.cardif.closingclaims.domain.util.exception.BusinessException;
import co.com.bnpparibas.cardif.closingclaims.domain.util.helpers.PeruAccountingReportExcelHelper;
import co.com.bnpparibas.cardif.closingclaims.domain.util.helpers.PeruAccountingReportMapper;
import co.com.bnpparibas.cardif.closingclaims.infraestructure.repository.PeruAccountingReportRepository;
import lombok.extern.slf4j.Slf4j;
import org.springframework.dao.DataAccessException;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.io.IOException;
import java.time.LocalDateTime;
import java.util.List;

/**
 * Implementación del servicio para gestionar el reporte contable de Perú.
 */
@Slf4j
@Service
public class PeruAccountingReportServiceImpl
        implements IPeruAccountingReportService {

    private final PeruAccountingReportRepository repository;
    private final PeruAccountingReportMapper mapper;
    private final PeruAccountingReportExcelHelper excelHelper;

    public PeruAccountingReportServiceImpl(
            PeruAccountingReportRepository repository,
            PeruAccountingReportMapper mapper,
            PeruAccountingReportExcelHelper excelHelper) {
        this.repository = repository;
        this.mapper = mapper;
        this.excelHelper = excelHelper;
    }

    @Override
    @Transactional(readOnly = true)
    public PeruAccountingReportResponseDTO getLatestReportDate(
            String pHeader,
            String correlationId,
            String requestId) {

        LocalDateTime reportDate = findLatestReportDate(
                correlationId,
                requestId);

        validateReportDate(reportDate);
        return mapper.toResponseDTO(reportDate);
    }

    @Override
    @Transactional
    public String generateReport(
            String pHeader,
            String correlationId,
            String requestId) {

        executeReportGeneration(correlationId, requestId);
        return "Información del reporte contable generada correctamente.";
    }

    @Override
    @Transactional(readOnly = true)
    public byte[] downloadReport(
            String pHeader,
            String correlationId,
            String requestId) {

        List<PeruAccountingReport> reports =
                findReportsForExport(correlationId, requestId);

        validateReports(reports);
        return generateExcel(reports, correlationId, requestId);
    }

    private LocalDateTime findLatestReportDate(
            String correlationId,
            String requestId) {
        try {
            return repository.findLatestReportDate();
        } catch (DataAccessException exception) {
            logDatabaseError(
                    "Error consultando la fecha del reporte",
                    correlationId,
                    requestId,
                    exception);
            throw databaseException(exception);
        }
    }

    private void executeReportGeneration(
            String correlationId,
            String requestId) {
        try {
            repository.generateReport();
        } catch (DataAccessException exception) {
            logDatabaseError(
                    "Error generando el reporte contable",
                    correlationId,
                    requestId,
                    exception);
            throw databaseException(exception);
        }
    }

    private List<PeruAccountingReport> findReportsForExport(
            String correlationId,
            String requestId) {
        try {
            return repository.findAllForExport();
        } catch (DataAccessException exception) {
            logDatabaseError(
                    "Error consultando los registros del reporte",
                    correlationId,
                    requestId,
                    exception);
            throw databaseException(exception);
        }
    }

    private byte[] generateExcel(
            List<PeruAccountingReport> reports,
            String correlationId,
            String requestId) {
        try {
            return excelHelper.generateExcel(reports);
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

    private void validateReportDate(LocalDateTime reportDate) {
        if (reportDate == null) {
            throw new BusinessException(
                    null,
                    "No existe una fecha de reporte para consultar",
                    HttpStatus.NOT_FOUND);
        }
    }

    private void validateReports(List<PeruAccountingReport> reports) {
        if (reports == null || reports.isEmpty()) {
            throw new BusinessException(
                    null,
                    "No existen registros para generar el archivo",
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
                "Error al acceder a la información del reporte contable",
                HttpStatus.INTERNAL_SERVER_ERROR);
    }
}
