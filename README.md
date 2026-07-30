package co.com.bnpparibas.cardif.closingclaims.domain.services.impl;

import co.com.bnpparibas.cardif.closingclaims.domain.dtos.loaddata.*;
import co.com.bnpparibas.cardif.closingclaims.domain.entity.FileData;
import co.com.bnpparibas.cardif.closingclaims.domain.entity.FileDataExt;
import co.com.bnpparibas.cardif.closingclaims.domain.services.IReportDataService;
import co.com.bnpparibas.cardif.closingclaims.domain.util.constants.FlagCode;
import co.com.bnpparibas.cardif.closingclaims.domain.util.exception.BusinessException;
import co.com.bnpparibas.cardif.closingclaims.domain.util.helpers.ReportDataMapper;
import co.com.bnpparibas.cardif.closingclaims.infraestructure.repository.FileDataExtRepository;
import co.com.bnpparibas.cardif.closingclaims.infraestructure.repository.FileDataRepository;
import co.com.bnpparibas.cardif.closingclaims.infraestructure.repository.ReportDataRepository;
import co.com.bnpparibas.cardif.closingclaims.infraestructure.repository.impl.ReportStoredProcedureRepository;
import org.apache.poi.ss.usermodel.Cell;
import org.apache.poi.ss.usermodel.CellStyle;
import org.apache.poi.ss.usermodel.Font;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.xssf.streaming.SXSSFWorkbook;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Base64;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class ReportDataServiceImpl implements IReportDataService {

    private static final Logger logger =
            LoggerFactory.getLogger(ReportDataServiceImpl.class);

    private final FileDataRepository fileDataRepository;
    private final FileDataExtRepository fileDataExtRepository;
    private final ReportDataRepository reportDataRepository;
    private final ReportStoredProcedureRepository reportStoredProcedureRepository;

    private static final String INVALID_KEY = ".";

    private static final String REPORT_TYPE_DATA = "datos";
    private static final String REPORT_TYPE_MOVEMENTS = "movimientos";

    /** Nombre de hoja y de archivo, igual al del legacy. */
    private static final String REPORT_NAME_DATA = "RptDatos";
    private static final String REPORT_NAME_MOVEMENTS = "RptMovimientos";

    private static final String SP_REPORT_DATA =
            "dbo.SP_Reporte_Datos_Siniestros";
    private static final String SP_REPORT_MOVEMENTS =
            "dbo.SP_Reporte_Movimientos_Siniestros";

    private static final String XLSX_CONTENT_TYPE =
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet";
    private static final String XLSX_EXTENSION = ".xlsx";

    private static final int ROWS_IN_MEMORY = 500;

    public ReportDataServiceImpl(
            FileDataRepository fileDataRepository,
            FileDataExtRepository fileDataExtRepository,
            ReportDataRepository reportDataRepository,
            ReportStoredProcedureRepository reportStoredProcedureRepository) {

        this.fileDataRepository = fileDataRepository;
        this.fileDataExtRepository = fileDataExtRepository;
        this.reportDataRepository = reportDataRepository;
        this.reportStoredProcedureRepository = reportStoredProcedureRepository;
    }

    @Override
    public ReportStatusPageDTO getReportData(String pHeader, String correlationId,
                                             String requestId, Integer page,
                                             Integer pageSize) {

        int pageNumber = (page == null) ? 0 : page;
        int size = (pageSize == null) ? 50 : pageSize;
        Pageable pageable = PageRequest.of(pageNumber, size);
        List<ReportStatusDTO> reportStatusDTOS;

        int currentPage;
        int totalPages;
        long totalElements;

        if (FlagCode.PERU.equalsIgnoreCase(pHeader)) {
            Page<FileDataExt> result = fileDataExtRepository.findAll(pageable);
            reportStatusDTOS = ReportDataMapper.INSTANCE
                    .fileDataExtListToReportStatusDTOList(result.getContent());

            currentPage = result.getNumber();
            totalPages = result.getTotalPages();
            totalElements = result.getTotalElements();

        } else {
            Page<FileData> result = fileDataRepository.findAll(pageable);
            reportStatusDTOS = ReportDataMapper.INSTANCE
                    .fileDataListToReportStatusDTOList(result.getContent());

            currentPage = result.getNumber();
            totalPages = result.getTotalPages();
            totalElements = result.getTotalElements();
        }

        return ReportStatusPageDTO.builder()
                .reportStatusDTOS(reportStatusDTOS)
                .currentPage(currentPage)
                .totalPages(totalPages)
                .remainingPages(totalPages - currentPage - 1)
                .totalElements(totalElements)
                .build();
    }

    @Override
    public String changeStatusFileData(String pHeader, String correlationId,
                                       String requestId) {
        try {
            if (FlagCode.PERU.equalsIgnoreCase(pHeader)) {
                fileDataExtRepository.changeStatusFile();
            } else {
                fileDataRepository.changeStatusFile();
            }
            return "Aceptado!! En Proceso.";
        } catch (Exception ex) {
            logger.error("Error cambiando estado del archivo. CorrelationId={}, RequestId={}",
                    correlationId, requestId, ex);
            throw new BusinessException(null,
                    "No se pudo cambiar el estado del archivo. Por favor, intente nuevamente.",
                    HttpStatus.PRECONDITION_FAILED);
        }
    }

    @Override
    public KeyClaimPageDTO getKeyClaims(String pHeader, String correlationId,
                                        String requestId, Integer page,
                                        Integer pageSize) {

        int pageNumber = (page == null) ? 0 : page;
        int size = (pageSize == null) ? 50 : pageSize;
        Pageable pageable = PageRequest.of(pageNumber, size);
        List<KeyClaimDTO> keyClaims;
        int currentPage;
        int totalPages;
        long totalElements;

        if (FlagCode.PERU.equalsIgnoreCase(pHeader)) {
            Page<FileDataExtRepository.LlaveSiniestroExtProjection> result =
                    fileDataExtRepository.findKeyClaims(pageable);

            keyClaims = result.getContent().stream()
                    .filter(k -> k != null && !INVALID_KEY.equals(k.getLlavesiniestros()))
                    .map(k -> new KeyClaimDTO(k.getLlavesiniestros()))
                    .collect(Collectors.toList());

            currentPage = result.getNumber();
            totalPages = result.getTotalPages();
            totalElements = result.getTotalElements();

        } else {
            Page<FileDataRepository.LlaveSiniestroProjection> result =
                    fileDataRepository.findKeyClaims(pageable);

            keyClaims = result.getContent().stream()
                    .filter(k -> k != null && !INVALID_KEY.equals(k.getLlavesiniestros()))
                    .map(k -> new KeyClaimDTO(k.getLlavesiniestros()))
                    .collect(Collectors.toList());

            currentPage = result.getNumber();
            totalPages = result.getTotalPages();
            totalElements = result.getTotalElements();
        }

        return KeyClaimPageDTO.builder()
                .keyClaimDTOS(keyClaims)
                .currentPage(currentPage)
                .totalPages(totalPages)
                .remainingPages(totalPages - currentPage - 1)
                .totalElements(totalElements)
                .build();
    }

    @Override
    public List<ReportStatusResponseDto> getReportStatus() {

        List<ReportDataRepository.ReportStatusProjection> reportStatus =
                reportDataRepository.findAllReportStatus();

        List<ReportStatusResponseDto> response = new ArrayList<>();

        if (reportStatus == null || reportStatus.isEmpty()) {
            return response;
        }

        for (ReportDataRepository.ReportStatusProjection projection : reportStatus) {
            ReportStatusResponseDto dto = new ReportStatusResponseDto();
            dto.setId(projection.getId());
            dto.setFechaproceso(projection.getFechaproceso());
            dto.setEstado(projection.getEstado());
            response.add(dto);
        }
        return response;
    }

    /**
     * Sin @Transactional: el procedimiento ejecuta decenas de UPDATE y
     * DELETE sobre tablas completas y en el legacy corria en autocommit.
     * Envolverlo en una sola transaccion escala bloqueos a nivel tabla.
     */
    @Override
    public void generateReport() {
        reportDataRepository.generateReport();
    }

    @Override
    @Transactional(readOnly = true)
    public ReportFileResponseDto getReport(final String reportType) {

        validateReportType(reportType);

        boolean isDataReport = REPORT_TYPE_DATA.equalsIgnoreCase(reportType);

        String storedProcedure = isDataReport ? SP_REPORT_DATA : SP_REPORT_MOVEMENTS;
        String reportName = isDataReport ? REPORT_NAME_DATA : REPORT_NAME_MOVEMENTS;

        ReportTabularDto reportInformation =
                reportStoredProcedureRepository.execute(storedProcedure);

        if (!reportInformation.hasColumns()) {
            logger.error("El procedimiento {} no devolvio un result set.", storedProcedure);
            throw new BusinessException(null,
                    "No fue posible obtener la informacion del reporte.",
                    HttpStatus.PRECONDITION_FAILED);
        }

        ReportFileResponseDto response = new ReportFileResponseDto();
        response.setFileType(XLSX_CONTENT_TYPE);
        response.setFileName(reportName + XLSX_EXTENSION);
        response.setFileBase64(Base64.getEncoder()
                .encodeToString(buildExcel(reportName, reportInformation)));

        return response;
    }

    private void validateReportType(final String reportType) {
        if (reportType == null
                || (!REPORT_TYPE_DATA.equalsIgnoreCase(reportType)
                && !REPORT_TYPE_MOVEMENTS.equalsIgnoreCase(reportType))) {
            throw new BusinessException(null,
                    "El tipo de reporte solicitado no es valido.",
                    HttpStatus.BAD_REQUEST);
        }
    }

    /**
     * Construye el xlsx con la fila de cabeceras tomada de la metadata
     * del procedimiento y todas las celdas como texto.
     */
    private byte[] buildExcel(final String sheetName,
                              final ReportTabularDto information) {

        SXSSFWorkbook workbook = new SXSSFWorkbook(ROWS_IN_MEMORY);

        try (ByteArrayOutputStream outputStream = new ByteArrayOutputStream()) {

            Sheet sheet = workbook.createSheet(sheetName);

            CellStyle headerStyle = workbook.createCellStyle();
            Font headerFont = workbook.createFont();
            headerFont.setBold(true);
            headerStyle.setFont(headerFont);

            int rowNumber = 0;

            List<String> headers = information.getHeaders();
            Row headerRow = sheet.createRow(rowNumber++);
            for (int column = 0; column < headers.size(); column++) {
                Cell cell = headerRow.createCell(column);
                cell.setCellStyle(headerStyle);
                cell.setCellValue(headers.get(column));
            }

            for (String[] values : information.getRows()) {
                Row row = sheet.createRow(rowNumber++);
                for (int column = 0; column < values.length; column++) {
                    row.createCell(column).setCellValue(values[column]);
                }
            }

            workbook.write(outputStream);
            return outputStream.toByteArray();

        } catch (IOException exception) {
            logger.error("Error generando el archivo {}.", sheetName, exception);
            throw new BusinessException(null,
                    "No fue posible generar el archivo del reporte.",
                    HttpStatus.INTERNAL_SERVER_ERROR);
        } finally {
            workbook.dispose();
            try {
                workbook.close();
            } catch (IOException exception) {
                logger.warn("No se pudo cerrar el libro de {}.", sheetName, exception);
            }
        }
    }

    @Override
    @Transactional(readOnly = true)
    public List<InconsistentCoverageResponseDto> getInconsistentCoverages() {

        List<ReportDataRepository.InconsistentCoverageProjection> coverages =
                reportDataRepository.findInconsistentCoverages();

        return ReportDataMapper.INSTANCE.projectionListToDtoList(coverages);
    }
}
