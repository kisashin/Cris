package co.com.bnpparibas.cardif.closingclaims.api;

import co.com.bnpparibas.cardif.closingclaims.domain.dtos.individualnews.ClaimMovementResponseDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.individualnews.IndividualNewsDeleteRequestDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.individualnews.IndividualNewsRequestDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.individualnews.IndividualNewsResponseDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.response.model.ResponseHeader;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.response.model.ResponseModel;
import co.com.bnpparibas.cardif.closingclaims.domain.services.IIndividualNewsService;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import javax.validation.Valid;
import java.util.List;

/**
 * API REST para la gestión de novedades individuales de movimientos.
 *
 * <p>Expone los endpoints necesarios para:</p>
 * <ul>
 *   <li>Consultar los movimientos de un siniestro sin novedad pendiente.</li>
 *   <li>Solicitar la actualización o la eliminación de un movimiento.</li>
 *   <li>Consultar las novedades pendientes de autorización.</li>
 *   <li>Aprobar o cancelar una novedad pendiente.</li>
 * </ul>
 */
@RestController
@RequestMapping("/v1")
@Tag(name = "Novedades individuales de movimientos")
@CrossOrigin("*")
public class IndividualNewsController {

    private final IIndividualNewsService individualNewsService;

    public IndividualNewsController(IIndividualNewsService individualNewsService) {
        this.individualNewsService = individualNewsService;
    }

    /**
     * Consulta los movimientos de un siniestro que no tienen novedad pendiente.
     *
     * @param pHeader       encabezado opcional de seguridad.
     * @param correlationId identificador de correlación.
     * @param requestId     identificador de la petición.
     * @param claimNumber   número de siniestro a consultar.
     * @return respuesta con los movimientos disponibles.
     */
    @GetMapping("/novedades-individuales/movimientos")
    public ResponseEntity<ResponseModel<List<ClaimMovementResponseDTO>>> findMovements(
            @RequestHeader(value = "_p", required = false) final String pHeader,
            @RequestHeader(value = "correlation_id", required = false) final String correlationId,
            @RequestHeader(value = "request_id", required = false) final String requestId,
            @RequestParam(value = "numeroSiniestro") final String claimNumber) {

        List<ClaimMovementResponseDTO> result =
                individualNewsService.findMovementsByClaimNumber(
                        pHeader, correlationId, requestId, claimNumber);

        ResponseModel<List<ClaimMovementResponseDTO>> response =
                new ResponseModel<>(correlationId,
                        ResponseHeader.builder().returnCode(HttpStatus.OK.value()).build(),
                        result);

        return new ResponseEntity<>(response, HttpStatus.OK);
    }

    /**
     * Consulta un movimiento por su identificador Carvajal.
     *
     * @param pHeader       encabezado opcional de seguridad.
     * @param correlationId identificador de correlación.
     * @param requestId     identificador de la petición.
     * @param idCarvajal    identificador del movimiento.
     * @return respuesta con el movimiento consultado.
     */
    @GetMapping("/novedades-individuales/movimientos/{idCarvajal}")
    public ResponseEntity<ResponseModel<ClaimMovementResponseDTO>> findMovementById(
            @RequestHeader(value = "_p", required = false) final String pHeader,
            @RequestHeader(value = "correlation_id", required = false) final String correlationId,
            @RequestHeader(value = "request_id", required = false) final String requestId,
            @PathVariable final Long idCarvajal) {

        ClaimMovementResponseDTO result =
                individualNewsService.findMovementById(
                        pHeader, correlationId, requestId, idCarvajal);

        ResponseModel<ClaimMovementResponseDTO> response =
                new ResponseModel<>(correlationId,
                        ResponseHeader.builder().returnCode(HttpStatus.OK.value()).build(),
                        result);

        return new ResponseEntity<>(response, HttpStatus.OK);
    }

    /**
     * Registra una solicitud de actualización sobre un movimiento.
     *
     * @param pHeader       encabezado opcional de seguridad.
     * @param correlationId identificador de correlación.
     * @param requestId     identificador de la petición.
     * @param user          usuario autenticado que realiza la solicitud.
     * @param request       nuevos valores del movimiento.
     * @return respuesta con la novedad creada.
     */
    @PostMapping("/novedades-individuales/actualizaciones")
    public ResponseEntity<ResponseModel<IndividualNewsResponseDTO>> createUpdateRequest(
            @RequestHeader(value = "_p", required = false) final String pHeader,
            @RequestHeader(value = "correlation_id", required = false) final String correlationId,
            @RequestHeader(value = "request_id", required = false) final String requestId,
            @RequestHeader(value = "UID_USER", required = false) final String user,
            @Valid @RequestBody final IndividualNewsRequestDTO request) {

        IndividualNewsResponseDTO created =
                individualNewsService.createUpdateRequest(
                        pHeader, correlationId, requestId, user, request);

        ResponseModel<IndividualNewsResponseDTO> response =
                new ResponseModel<>(correlationId,
                        ResponseHeader.builder().returnCode(HttpStatus.CREATED.value()).build(),
                        created);

        return new ResponseEntity<>(response, HttpStatus.CREATED);
    }

    /**
     * Registra una solicitud de eliminación sobre un movimiento.
     *
     * @param pHeader       encabezado opcional de seguridad.
     * @param correlationId identificador de correlación.
     * @param requestId     identificador de la petición.
     * @param user          usuario autenticado que realiza la solicitud.
     * @param request       identificador y justificación.
     * @return respuesta con la novedad creada.
     */
    @PostMapping("/novedades-individuales/eliminaciones")
    public ResponseEntity<ResponseModel<IndividualNewsResponseDTO>> createDeleteRequest(
            @RequestHeader(value = "_p", required = false) final String pHeader,
            @RequestHeader(value = "correlation_id", required = false) final String correlationId,
            @RequestHeader(value = "request_id", required = false) final String requestId,
            @RequestHeader(value = "UID_USER", required = false) final String user,
            @Valid @RequestBody final IndividualNewsDeleteRequestDTO request) {

        IndividualNewsResponseDTO created =
                individualNewsService.createDeleteRequest(
                        pHeader, correlationId, requestId, user, request);

        ResponseModel<IndividualNewsResponseDTO> response =
                new ResponseModel<>(correlationId,
                        ResponseHeader.builder().returnCode(HttpStatus.CREATED.value()).build(),
                        created);

        return new ResponseEntity<>(response, HttpStatus.CREATED);
    }

    /**
     * Consulta las novedades pendientes de autorización.
     *
     * @param pHeader       encabezado opcional de seguridad.
     * @param correlationId identificador de correlación.
     * @param requestId     identificador de la petición.
     * @return respuesta con las novedades pendientes.
     */
    @GetMapping("/novedades-individuales")
    public ResponseEntity<ResponseModel<List<IndividualNewsResponseDTO>>> findPendingNews(
            @RequestHeader(value = "_p", required = false) final String pHeader,
            @RequestHeader(value = "correlation_id", required = false) final String correlationId,
            @RequestHeader(value = "request_id", required = false) final String requestId) {

        List<IndividualNewsResponseDTO> result =
                individualNewsService.findPendingNews(pHeader, correlationId, requestId);

        ResponseModel<List<IndividualNewsResponseDTO>> response =
                new ResponseModel<>(correlationId,
                        ResponseHeader.builder().returnCode(HttpStatus.OK.value()).build(),
                        result);

        return new ResponseEntity<>(response, HttpStatus.OK);
    }

    /**
     * Consulta el detalle de una novedad pendiente.
     *
     * @param pHeader       encabezado opcional de seguridad.
     * @param correlationId identificador de correlación.
     * @param requestId     identificador de la petición.
     * @param code          identificador de la novedad.
     * @return respuesta con la novedad consultada.
     */
    @GetMapping("/novedades-individuales/{code}")
    public ResponseEntity<ResponseModel<IndividualNewsResponseDTO>> findPendingNewsByCode(
            @RequestHeader(value = "_p", required = false) final String pHeader,
            @RequestHeader(value = "correlation_id", required = false) final String correlationId,
            @RequestHeader(value = "request_id", required = false) final String requestId,
            @PathVariable final Long code) {

        IndividualNewsResponseDTO result =
                individualNewsService.findPendingNewsByCode(
                        pHeader, correlationId, requestId, code);

        ResponseModel<IndividualNewsResponseDTO> response =
                new ResponseModel<>(correlationId,
                        ResponseHeader.builder().returnCode(HttpStatus.OK.value()).build(),
                        result);

        return new ResponseEntity<>(response, HttpStatus.OK);
    }

    /**
     * Aplica una novedad pendiente sobre el histórico de movimientos.
     *
     * @param pHeader       encabezado opcional de seguridad.
     * @param correlationId identificador de correlación.
     * @param requestId     identificador de la petición.
     * @param user          usuario autenticado que autoriza.
     * @param code          identificador de la novedad.
     * @return respuesta con la novedad procesada.
     */
    @PostMapping("/novedades-individuales/{code}/aprobar")
    public ResponseEntity<ResponseModel<IndividualNewsResponseDTO>> approveNews(
            @RequestHeader(value = "_p", required = false) final String pHeader,
            @RequestHeader(value = "correlation_id", required = false) final String correlationId,
            @RequestHeader(value = "request_id", required = false) final String requestId,
            @RequestHeader(value = "UID_USER", required = false) final String user,
            @PathVariable final Long code) {

        IndividualNewsResponseDTO processed =
                individualNewsService.approveNews(
                        pHeader, correlationId, requestId, user, code);

        ResponseModel<IndividualNewsResponseDTO> response =
                new ResponseModel<>(correlationId,
                        ResponseHeader.builder().returnCode(HttpStatus.OK.value()).build(),
                        processed);

        return new ResponseEntity<>(response, HttpStatus.OK);
    }

    /**
     * Cancela una novedad pendiente.
     *
     * @param pHeader       encabezado opcional de seguridad.
     * @param correlationId identificador de correlación.
     * @param requestId     identificador de la petición.
     * @param user          usuario autenticado que cancela.
     * @param code          identificador de la novedad.
     * @return respuesta con la novedad cancelada.
     */
    @PostMapping("/novedades-individuales/{code}/cancelar")
    public ResponseEntity<ResponseModel<IndividualNewsResponseDTO>> cancelNews(
            @RequestHeader(value = "_p", required = false) final String pHeader,
            @RequestHeader(value = "correlation_id", required = false) final String correlationId,
            @RequestHeader(value = "request_id", required = false) final String requestId,
            @RequestHeader(value = "UID_USER", required = false) final String user,
            @PathVariable final Long code) {

        IndividualNewsResponseDTO cancelled =
                individualNewsService.cancelNews(
                        pHeader, correlationId, requestId, user, code);

        ResponseModel<IndividualNewsResponseDTO> response =
                new ResponseModel<>(correlationId,
                        ResponseHeader.builder().returnCode(HttpStatus.OK.value()).build(),
                        cancelled);

        return new ResponseEntity<>(response, HttpStatus.OK);
    }
}