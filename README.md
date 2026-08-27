package co.com.bnpparibas.cardif.closingclaims.domain.services.impl;

import co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingaval.ClosingAval;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia.ColombiaAccountingLine;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia.ColombiaAccountingResultDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia.ColombiaXmlFile;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia.ColombiaXmlFileDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.entity.ArchivoAsientoAvalXml;
import co.com.bnpparibas.cardif.closingclaims.domain.entity.TmpRepAvalCierre;
import co.com.bnpparibas.cardif.closingclaims.domain.services.IClosingAvalService;
import co.com.bnpparibas.cardif.closingclaims.domain.util.exception.BusinessException;
import co.com.bnpparibas.cardif.closingclaims.domain.util.helpers.ColombiaAccountingXmlHelper;
import co.com.bnpparibas.cardif.closingclaims.domain.util.messages.ColombiaClosingMessage;
import co.com.bnpparibas.cardif.closingclaims.infraestructure.repository.ArchivoAsientoAvalXmlRepository;
import co.com.bnpparibas.cardif.closingclaims.infraestructure.repository.ClosingAvalRepository;
import co.com.bnpparibas.cardif.closingclaims.infraestructure.repository.StoredProcedureExecutor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.dao.DataAccessException;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.UUID;
import java.util.stream.Collectors;

@Slf4j
@Service
public class ClosingAvalServiceImpl implements IClosingAvalService {

    private static final String AVAL_CALL =
            "EXEC dbo.sp_contabiliza_aval";

    private static final String REQUIRED_COLUMN = "Familia";

    private static final String SUCCESS_MESSAGE =
            "Asientos generados con éxito.";
    private static final String GENERATED_STATUS = "GENERADO";

    private static final DateTimeFormatter PROCESS_DATE_FORMAT =
            DateTimeFormatter.ofPattern(
                    "dd/MM/yyyy hh:mm:ss a", new Locale("es", "CO"));

    private final ClosingAvalRepository closingAvalRepository;
    private final ArchivoAsientoAvalXmlRepository fileRepository;
    private final ColombiaAccountingXmlHelper xmlHelper;
    private final StoredProcedureExecutor storedProcedureExecutor;

    public ClosingAvalServiceImpl(
            ClosingAvalRepository closingAvalRepository,
            ArchivoAsientoAvalXmlRepository fileRepository,
            ColombiaAccountingXmlHelper xmlHelper,
            StoredProcedureExecutor storedProcedureExecutor) {
        this.closingAvalRepository = closingAvalRepository;
        this.fileRepository = fileRepository;
        this.xmlHelper = xmlHelper;
        this.storedProcedureExecutor = storedProcedureExecutor;
    }

    @Override
    public List<ClosingAval> getDetailsReportsAval(String pHeader, String correlationId, String requestId) {
        List<TmpRepAvalCierre> details = closingAvalRepository.findAllDetailsAval();

        if (details == null || details.isEmpty()) {
            throw new BusinessException(null, "No registros para consultar", HttpStatus.BAD_REQUEST);
        }

        return details.stream()
                .map(p -> ClosingAval.builder()
                        .status(p.getEstado())
                        .dateGenerate(p.getFechagenera())
                        .nombreRpt(p.getNombreRpt())
                        .build())
                .collect(Collectors.toList());
    }

    @Override
    public String uploadReportsPendingRptAval(String pHeader, String correlationId, String requestId) {
        try{
            int rowsUpdated = closingAvalRepository.markAsPendingRptAval();

            return "Actualización completada, filas afectadas: " + rowsUpdated;
        }catch(Exception e) {
            throw new BusinessException(e, null, "Error al actualizar reporte", HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    public List<ClosingAval> getReportsSeatAval(String pHeader, String correlationId, String requestId) {
        List<ClosingAvalRepository.ArchivoAsientoAvalProjection> reports = closingAvalRepository.findAllReportsAsientoAval();

        if (reports == null || reports.isEmpty()) {
            throw new BusinessException(null, "No registros para consultar", HttpStatus.BAD_REQUEST);
        }

        return reports.stream()
                .map(p -> ClosingAval.builder()
                        .status(p.getEstado())
                        .dateGenerate(p.getFechaproceso())
                        .nombreRpt(p.getNombreArchivo())
                        .build())
                .collect(Collectors.toList());
    }

    @Override
    public String uploadReportsPendingRptSeatAval(String pHeader, String correlationId, String requestId) {
        try {
            int rowsUpdated = closingAvalRepository.markAsPendingRptSeatAval();

            return "Actualización completada, filas afectadas: " + rowsUpdated;
        } catch (Exception e) {
            throw new BusinessException(e, null, "Error al actualizar reporte", HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    @Transactional
    public ColombiaAccountingResultDTO generateAccountingEntries(
            String pHeader,
            String correlationId,
            String requestId) {

        deletePreviousFiles(correlationId, requestId);

        List<ColombiaAccountingLine> lines =
                executeProcedure(AVAL_CALL, correlationId, requestId);

        List<ColombiaXmlFile> files =
                buildFiles(lines, correlationId, requestId);

        if (files.isEmpty()) {
            throw new BusinessException(
                    null,
                    ColombiaClosingMessage
                            .NO_ACCOUNTING_ENTRIES_GENERATED.getMessage(),
                    HttpStatus.NOT_FOUND);
        }

        String period = lines.get(0).getPeriod();
        List<ArchivoAsientoAvalXml> saved =
                saveFiles(files, correlationId, requestId);

        return ColombiaAccountingResultDTO.builder()
                .message(SUCCESS_MESSAGE)
                .period(period)
                .files(toXmlDto(saved))
                .build();
    }

    @Override
    @Transactional(readOnly = true)
    public List<ColombiaXmlFileDTO> findGeneratedFiles(
            String correlationId,
            String requestId) {
        try {
            return toXmlDto(fileRepository.findLatest());
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
    public ArchivoAsientoAvalXml findXmlFile(
            Integer id,
            String correlationId,
            String requestId) {

        ArchivoAsientoAvalXml file;

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
                    ColombiaClosingMessage.XML_FILE_NOT_FOUND.getMessage(),
                    HttpStatus.NOT_FOUND);
        }

        return file;
    }

    private void deletePreviousFiles(
            String correlationId,
            String requestId) {
        try {
            fileRepository.deleteAllFiles();
        } catch (DataAccessException exception) {
            logDatabaseError(
                    "Error eliminando los archivos XML anteriores",
                    correlationId,
                    requestId,
                    exception);
            throw databaseException(exception);
        }
    }

    private List<ColombiaAccountingLine> executeProcedure(
            String call,
            String correlationId,
            String requestId) {
        try {
            return storedProcedureExecutor.query(
                    call,
                    resultSet -> ColombiaAccountingLine.builder()
                            .family(resultSet.getString("Familia"))
                            .period(resultSet.getString("Periodo"))
                            .pass(resultSet.getInt("Pasada"))
                            .movementType(resultSet.getString("Mv"))
                            .fileName(resultSet.getString("NombreArchivo"))
                            .sequence(resultSet.getLong("Secuencia"))
                            .content(resultSet.getString("Line"))
                            .build(),
                    REQUIRED_COLUMN);
        } catch (DataAccessException exception) {
            logDatabaseError(
                    "Error ejecutando la contabilización",
                    correlationId,
                    requestId,
                    exception);
            throw databaseException(exception);
        }
    }

    private List<ColombiaXmlFile> buildFiles(
            List<ColombiaAccountingLine> lines,
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
                    ColombiaClosingMessage.XML_GENERATION_ERROR.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    private List<ArchivoAsientoAvalXml> saveFiles(
            List<ColombiaXmlFile> files,
            String correlationId,
            String requestId) {

        String batchId = UUID.randomUUID().toString();
        LocalDateTime processDate = LocalDateTime.now();
        List<ArchivoAsientoAvalXml> entities = new ArrayList<>();

        for (ColombiaXmlFile file : files) {
            entities.add(ArchivoAsientoAvalXml.builder()
                    .idLote(batchId)
                    .periodo(file.getPeriod())
                    .familia(file.getFamily())
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

    private List<ColombiaXmlFileDTO> toXmlDto(
            List<ArchivoAsientoAvalXml> files) {

        return files.stream()
                .map(file -> ColombiaXmlFileDTO.builder()
                        .id(file.getId())
                        .period(file.getPeriodo())
                        .family(file.getFamilia())
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
                ColombiaClosingMessage.DATABASE_ACCESS_ERROR.getMessage(),
                HttpStatus.INTERNAL_SERVER_ERROR);
    }
}
