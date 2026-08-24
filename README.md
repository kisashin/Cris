package co.com.bnpparibas.cardif.closingclaims.api;

import co.com.bnpparibas.cardif.closingclaims.domain.dtos.cardifcenterclosing.AccountingXmlFileDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.cardifcenterclosing.CenterAccountingResultDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.response.model.ResponseHeader;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.response.model.ResponseModel;
import co.com.bnpparibas.cardif.closingclaims.domain.entity.ArchivoAsientoCentro;
import co.com.bnpparibas.cardif.closingclaims.domain.services.ICardifCenterClosingService;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.nio.charset.StandardCharsets;
import java.util.List;

/**
 * API REST del cierre de movimientos Cardif Centroamerica.
 */
@RestController
@RequestMapping("/v1")
@Tag(name = "Cardif Center Closing")
@CrossOrigin("*")
public class CardifCenterClosingController {

    private static final String EXCEL_CONTENT_TYPE =
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet";
    private static final String XML_CONTENT_TYPE = "application/xml";

    @Value("${cardif.center.closing.report-filename:ReporteMovimientosCentro.xlsx}")
    private String fileName;

    private final ICardifCenterClosingService service;

    public CardifCenterClosingController(
            ICardifCenterClosingService service) {
        this.service = service;
    }

    /**
     * Ejecuta la contabilizacion y persiste los XML generados.
     */
    @PutMapping(
            path = "/cardif-center-closing/generate",
            produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResponseModel<CenterAccountingResultDTO>>
            generateAccountingEntries(
            @RequestHeader(value = "_p", required = false)
            String pHeader,
            @RequestHeader(value = "correlation_id", required = false)
            String correlationId,
            @RequestHeader(value = "request_id", required = false)
            String requestId) {

        CenterAccountingResultDTO result = service.generateAccountingEntries(
                pHeader,
                correlationId,
                requestId);

        return buildResponse(correlationId, result);
    }

    /**
     * Consulta los archivos XML generados en procesos anteriores.
     */
    @GetMapping(
            path = "/cardif-center-closing/files",
            produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResponseModel<List<AccountingXmlFileDTO>>>
            findGeneratedFiles(
            @RequestHeader(value = "correlation_id", required = false)
            String correlationId,
            @RequestHeader(value = "request_id", required = false)
            String requestId) {

        List<AccountingXmlFileDTO> files = service.findGeneratedFiles(
                correlationId,
                requestId);

        return buildResponse(correlationId, files);
    }

    /**
     * Descarga un archivo XML persistido.
     */
    @GetMapping(
            path = "/cardif-center-closing/files/{id}/download",
            produces = XML_CONTENT_TYPE)
    public ResponseEntity<byte[]> downloadXmlFile(
            @PathVariable("id") Integer id,
            @RequestHeader(value = "correlation_id", required = false)
            String correlationId,
            @RequestHeader(value = "request_id", required = false)
            String requestId) {

        ArchivoAsientoCentro file = service.findXmlFile(
                id,
                correlationId,
                requestId);

        byte[] content = file.getContenido()
                .getBytes(StandardCharsets.UTF_8);

        return ResponseEntity.ok()
                .header(
                        HttpHeaders.CONTENT_DISPOSITION,
                        "attachment; filename=\""
                                + file.getNombreArchivo() + "\"")
                .contentType(MediaType.parseMediaType(XML_CONTENT_TYPE))
                .contentLength(content.length)
                .body(content);
    }

    /**
     * Descarga el reporte de movimientos en formato Excel.
     */
    @GetMapping(
            path = "/cardif-center-closing/download",
            produces = EXCEL_CONTENT_TYPE)
    public ResponseEntity<byte[]> downloadMovementsReport(
            @RequestHeader(value = "_p", required = false)
            String pHeader,
            @RequestHeader(value = "correlation_id", required = false)
            String correlationId,
            @RequestHeader(value = "request_id", required = false)
            String requestId) {

        byte[] file = service.downloadMovementsReport(
                pHeader,
                correlationId,
                requestId);

        return ResponseEntity.ok()
                .header(
                        HttpHeaders.CONTENT_DISPOSITION,
                        "attachment; filename=\"" + fileName + "\"")
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
