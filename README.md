package co.com.bnpparibas.cardif.closingclaims.api;

import co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcardif.ClosingCardif;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia.ColombiaAccountingResultDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia.ColombiaXmlFileDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.response.model.ResponseHeader;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.response.model.ResponseModel;
import co.com.bnpparibas.cardif.closingclaims.domain.entity.ArchivoAsientoCardifXml;
import co.com.bnpparibas.cardif.closingclaims.domain.services.IClosingCardifService;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.nio.charset.StandardCharsets;
import java.util.List;

/**
 * API REST para la consulta y actualizacion de reportes Cierre Mensual de Directas (Cardif).
 *
 * <p>Expone los endpoints necesarios para:</p>
 * <ul>
 *   <li>Consultar los reportes de Cierre Mensual de Directas (Cardif)</li>
 *   <li>Actualizar los asientos contables, reportes cardif</li>
 *   <li>Generar, consultar y descargar los archivos XML contables</li>
 * </ul>
 *
 * <p>Todos los métodos aceptan los encabezados de trazabilidad habituales
 * (<code>_p</code>,
 * <code>correlation_id</code> y <code>request_id</code>) que son
 * propagados al servicio.</p>
 */
@RestController
@RequestMapping("/v1")
@Tag(name = "Cierre Cardif")
@CrossOrigin("*")
public class ClosingCardifController {

    private static final String XML_CONTENT_TYPE = "application/xml";

    private final IClosingCardifService closingCardifService;

    public ClosingCardifController(IClosingCardifService closingCardifService) {
        this.closingCardifService = closingCardifService;
    }

    /**
     * Consultar los reportes de Cierre Cardif
     *
     * @param pHeader        encabezado opcional de seguridad.
     * @param correlationId  identificador de correlación para trazabilidad.
     * @param requestId      identificador de la petición.
     * @return mensaje de confirmación del proceso.
     */
    @GetMapping(path = "/all-cardif-reports", produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResponseModel<List<ClosingCardif>>> getReportsCardif(
            @RequestHeader(value = "_p", required = false) String pHeader,
            @RequestHeader(value = "correlation_id", required = false) String correlationId,
            @RequestHeader(value = "request_id", required = false) String requestId) {

        List<ClosingCardif> reports = closingCardifService.getDetailsReportsCardif(pHeader, correlationId, requestId);
        ResponseModel<List<ClosingCardif>> listResponseModel = new ResponseModel<>(correlationId,
                ResponseHeader.builder().returnCode(HttpStatus.OK.value()).build(),
                reports);
        return new ResponseEntity<>(listResponseModel, HttpStatus.OK);
    }

    /**
     * Actualizar el reporte Cierre Cardif a estado Pendiente
     *
     * @param pHeader        encabezado opcional de seguridad.
     * @param correlationId  identificador de correlación para trazabilidad.
     * @param requestId      identificador de la petición.
     * @return mensaje de confirmación del proceso.
     */
    @PutMapping(path = "/update-cardif-report")
    public ResponseEntity<ResponseModel<String>> updateReportsAval(
            @RequestHeader(value = "_p", required = false) String pHeader,
            @RequestHeader(value = "correlation_id", required = false) String correlationId,
            @RequestHeader(value = "request_id", required = false) String requestId) {

        String result = closingCardifService.uploadReportsPendingRptCardif(
                pHeader,
                correlationId,
                requestId);

        ResponseModel<String> response = new ResponseModel<>(correlationId,
                ResponseHeader.builder().returnCode(HttpStatus.OK.value()).build(), result);
        return new ResponseEntity<>(response, HttpStatus.OK);
    }

    /**
     * Ejecuta la generación de los asientos contables.
     *
     * @param pHeader        encabezado opcional de seguridad.
     * @param correlationId  identificador de correlación para trazabilidad.
     * @param requestId      identificador de la petición.
     * @return resultado del proceso con los archivos generados.
     */
    @PutMapping(
            path = "/cardif-closing/generate",
            produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResponseModel<ColombiaAccountingResultDTO>>
            generateAccountingEntries(
            @RequestHeader(value = "_p", required = false) String pHeader,
            @RequestHeader(value = "correlation_id", required = false) String correlationId,
            @RequestHeader(value = "request_id", required = false) String requestId) {

        ColombiaAccountingResultDTO result =
                closingCardifService.generateAccountingEntries(
                        pHeader,
                        correlationId,
                        requestId);

        ResponseModel<ColombiaAccountingResultDTO> response =
                new ResponseModel<>(correlationId,
                        ResponseHeader.builder()
                                .returnCode(HttpStatus.OK.value()).build(),
                        result);
        return new ResponseEntity<>(response, HttpStatus.OK);
    }

    /**
     * Consulta los archivos XML generados en procesos anteriores.
     *
     * @param correlationId  identificador de correlación para trazabilidad.
     * @param requestId      identificador de la petición.
     * @return lista de archivos disponibles para descarga.
     */
    @GetMapping(
            path = "/cardif-closing/files",
            produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResponseModel<List<ColombiaXmlFileDTO>>>
            findGeneratedFiles(
            @RequestHeader(value = "correlation_id", required = false) String correlationId,
            @RequestHeader(value = "request_id", required = false) String requestId) {

        List<ColombiaXmlFileDTO> files =
                closingCardifService.findGeneratedFiles(
                        correlationId,
                        requestId);

        ResponseModel<List<ColombiaXmlFileDTO>> response =
                new ResponseModel<>(correlationId,
                        ResponseHeader.builder()
                                .returnCode(HttpStatus.OK.value()).build(),
                        files);
        return new ResponseEntity<>(response, HttpStatus.OK);
    }

    /**
     * Descarga un archivo XML persistido.
     *
     * @param id             identificador del archivo.
     * @param correlationId  identificador de correlación para trazabilidad.
     * @param requestId      identificador de la petición.
     * @return contenido del archivo XML.
     */
    @GetMapping(
            path = "/cardif-closing/files/{id}/download",
            produces = XML_CONTENT_TYPE)
    public ResponseEntity<byte[]> downloadXmlFile(
            @PathVariable("id") Integer id,
            @RequestHeader(value = "correlation_id", required = false) String correlationId,
            @RequestHeader(value = "request_id", required = false) String requestId) {

        ArchivoAsientoCardifXml file = closingCardifService.findXmlFile(
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
}
