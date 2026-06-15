src/main/java/co/com/bnpparibas/cardif/closingclaims/api/PeruAccountingReportController.java

package co.com.bnpparibas.cardif.closingclaims.api;

import co.com.bnpparibas.cardif.closingclaims.domain.dtos.peruaccountingreport.PeruAccountingReportResponseDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.response.model.ResponseHeader;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.response.model.ResponseModel;
import co.com.bnpparibas.cardif.closingclaims.domain.services.IPeruAccountingReportService;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * API REST para gestionar el reporte contable de Perú.
 */
@RestController
@RequestMapping("/v1")
@Tag(name = "Peru Accounting Report")
@CrossOrigin("*")
public class PeruAccountingReportController {

    private static final String EXCEL_CONTENT_TYPE =
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet";

    private static final String FILE_NAME =
            "ReporteContablePeru.xlsx";

    private final IPeruAccountingReportService service;

    public PeruAccountingReportController(
            IPeruAccountingReportService service) {
        this.service = service;
    }

    /**
     * Consulta la fecha de la última generación del reporte.
     */
    @GetMapping(
            path = "/peru-accounting-report/latest",
            produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResponseModel<PeruAccountingReportResponseDTO>>
            getLatestReportDate(
                    @RequestHeader(value = "_p", required = false)
                    String pHeader,
                    @RequestHeader(
                            value = "correlation_id",
                            required = false)
                    String correlationId,
                    @RequestHeader(
                            value = "request_id",
                            required = false)
                    String requestId) {

        PeruAccountingReportResponseDTO result =
                service.getLatestReportDate(
                        pHeader,
                        correlationId,
                        requestId);

        return buildResponse(correlationId, result);
    }

    /**
     * Genera la información del reporte contable.
     */
    @PutMapping(
            path = "/peru-accounting-report/generate",
            produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResponseModel<String>> generateReport(
            @RequestHeader(value = "_p", required = false)
            String pHeader,
            @RequestHeader(
                    value = "correlation_id",
                    required = false)
            String correlationId,
            @RequestHeader(
                    value = "request_id",
                    required = false)
            String requestId) {

        String result = service.generateReport(
                pHeader,
                correlationId,
                requestId);

        return buildResponse(correlationId, result);
    }

    /**
     * Descarga el reporte contable en formato Excel.
     */
    @GetMapping(
            path = "/peru-accounting-report/download",
            produces = EXCEL_CONTENT_TYPE)
    public ResponseEntity<byte[]> downloadReport(
            @RequestHeader(value = "_p", required = false)
            String pHeader,
            @RequestHeader(
                    value = "correlation_id",
                    required = false)
            String correlationId,
            @RequestHeader(
                    value = "request_id",
                    required = false)
            String requestId) {

        byte[] file = service.downloadReport(
                pHeader,
                correlationId,
                requestId);

        return ResponseEntity.ok()
                .header(
                        HttpHeaders.CONTENT_DISPOSITION,
                        "attachment; filename=\"" + FILE_NAME + "\"")
                .contentType(MediaType.parseMediaType(EXCEL_CONTENT_TYPE))
                .contentLength(file.length)
                .body(file);
    }

    private <T> ResponseEntity<ResponseModel<T>> buildResponse(
            String correlationId,
            T data) {

        ResponseModel<T> response = new ResponseModel<>(
                correlationId,
                ResponseHeader.builder()
                        .returnCode(HttpStatus.OK.value())
                        .build(),
                data);

        return new ResponseEntity<>(response, HttpStatus.OK);
    }
}
