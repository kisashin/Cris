package co.com.bnpparibas.cardif.closingclaims.api;

import co.com.bnpparibas.cardif.closingclaims.domain.dtos.response.model.ResponseHeader;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.response.model.ResponseModel;
import co.com.bnpparibas.cardif.closingclaims.domain.services.ICardifPeruClosingService;
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
 * API REST del cierre de movimientos Cardif Perú (legacy {@code _ext}).
 *
 * <p>Reemplaza la pantalla {@code AsientoCardif_ext.aspx} con dos operaciones
 * independientes: contabilizar (botón "Genera XML") y descargar el reporte
 * (botón "Consultar"). La descarga NO ejecuta el procedimiento.</p>
 */
@RestController
@RequestMapping("/v1")
@Tag(name = "Cardif Peru Closing")
@CrossOrigin("*")
public class CardifPeruClosingController {

    private static final String EXCEL_CONTENT_TYPE =
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet";

    private static final String FILE_NAME =
            "ReporteMovimientosCardifPeru.xlsx";

    private final ICardifPeruClosingService service;

    public CardifPeruClosingController(
            ICardifPeruClosingService service) {
        this.service = service;
    }

    /**
     * Ejecuta la contabilización de los movimientos pendientes.
     */
    @PutMapping(
            path = "/cardif-peru-closing/generate",
            produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResponseModel<String>> generateAccountingEntries(
            @RequestHeader(value = "_p", required = false)
            String pHeader,
            @RequestHeader(value = "correlation_id", required = false)
            String correlationId,
            @RequestHeader(value = "request_id", required = false)
            String requestId) {

        String result = service.generateAccountingEntries(
                pHeader,
                correlationId,
                requestId);

        return buildResponse(correlationId, result);
    }

    /**
     * Descarga el reporte de movimientos en formato Excel.
     */
    @GetMapping(
            path = "/cardif-peru-closing/download",
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
