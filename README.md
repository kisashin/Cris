package co.com.bnpparibas.cardif.closingclaims.api;

import co.com.bnpparibas.cardif.closingclaims.domain.dtos.individualnews.ClaimMovementResponseDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.individualnews.IndividualNewsDeleteRequestDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.individualnews.IndividualNewsRequestDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.individualnews.IndividualNewsResponseDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.response.model.ResponseModel;
import co.com.bnpparibas.cardif.closingclaims.domain.services.IIndividualNewsService;
import co.com.bnpparibas.cardif.closingclaims.domain.util.anums.NewsStatus;
import co.com.bnpparibas.cardif.closingclaims.domain.util.anums.NewsType;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import java.util.Collections;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyLong;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class IndividualNewsControllerTest {

    private static final String P_HEADER = "p-header";
    private static final String CORRELATION_ID = "correlation-id";
    private static final String REQUEST_ID = "request-id";
    private static final String USER = "f93141";
    private static final String CLAIM_NUMBER = "SIN-0001";
    private static final Long ID_CARVAJAL = 100L;
    private static final Long CODE = 55L;

    @Mock
    private IIndividualNewsService individualNewsService;

    @InjectMocks
    private IndividualNewsController individualNewsController;

    private ClaimMovementResponseDTO buildMovementResponse() {
        return ClaimMovementResponseDTO.builder()
                .idCarvajal(ID_CARVAJAL)
                .claimNumber(CLAIM_NUMBER)
                .movementType("PAGO")
                .build();
    }

    private IndividualNewsResponseDTO buildNewsResponse(NewsStatus status) {
        return IndividualNewsResponseDTO.builder()
                .code(CODE)
                .idCarvajal(ID_CARVAJAL)
                .claimNumber(CLAIM_NUMBER)
                .newsType(NewsType.ACTUALIZA.name())
                .status(status.name())
                .justification("Corrige socio")
                .requestUser(USER)
                .build();
    }

    @Test
    @DisplayName("findMovements responde OK con los movimientos disponibles")
    void findMovementsReturnsOk() {
        when(individualNewsService.findMovementsByClaimNumber(
                anyString(), anyString(), anyString(), anyString()))
                .thenReturn(Collections.singletonList(buildMovementResponse()));

        ResponseEntity<ResponseModel<List<ClaimMovementResponseDTO>>> response =
                individualNewsController.findMovements(
                        P_HEADER, CORRELATION_ID, REQUEST_ID, CLAIM_NUMBER);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals(CORRELATION_ID, response.getBody().getCorrelationId());
        assertEquals(HttpStatus.OK.value(),
                response.getBody().getResponseHeader().getReturnCode());
        assertEquals(1, response.getBody().getBodyResponse().size());
        verify(individualNewsService).findMovementsByClaimNumber(
                P_HEADER, CORRELATION_ID, REQUEST_ID, CLAIM_NUMBER);
    }

    @Test
    @DisplayName("findMovementById responde OK con el movimiento consultado")
    void findMovementByIdReturnsOk() {
        when(individualNewsService.findMovementById(
                anyString(), anyString(), anyString(), anyLong()))
                .thenReturn(buildMovementResponse());

        ResponseEntity<ResponseModel<ClaimMovementResponseDTO>> response =
                individualNewsController.findMovementById(
                        P_HEADER, CORRELATION_ID, REQUEST_ID, ID_CARVAJAL);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals(ID_CARVAJAL, response.getBody().getBodyResponse().getIdCarvajal());
    }

    @Test
    @DisplayName("createUpdateRequest responde CREATED con la novedad creada")
    void createUpdateRequestReturnsCreated() {
        when(individualNewsService.createUpdateRequest(anyString(), anyString(),
                anyString(), anyString(), any(IndividualNewsRequestDTO.class)))
                .thenReturn(buildNewsResponse(NewsStatus.PENDIENTE));

        IndividualNewsRequestDTO request = IndividualNewsRequestDTO.builder()
                .idCarvajal(ID_CARVAJAL)
                .build();

        ResponseEntity<ResponseModel<IndividualNewsResponseDTO>> response =
                individualNewsController.createUpdateRequest(
                        P_HEADER, CORRELATION_ID, REQUEST_ID, USER, request);

        assertEquals(HttpStatus.CREATED, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals(HttpStatus.CREATED.value(),
                response.getBody().getResponseHeader().getReturnCode());
        assertEquals(NewsStatus.PENDIENTE.name(),
                response.getBody().getBodyResponse().getStatus());
    }

    @Test
    @DisplayName("createDeleteRequest responde CREATED con la novedad creada")
    void createDeleteRequestReturnsCreated() {
        when(individualNewsService.createDeleteRequest(anyString(), anyString(),
                anyString(), anyString(), any(IndividualNewsDeleteRequestDTO.class)))
                .thenReturn(buildNewsResponse(NewsStatus.PENDIENTE));

        IndividualNewsDeleteRequestDTO request = IndividualNewsDeleteRequestDTO.builder()
                .idCarvajal(ID_CARVAJAL)
                .justification("Movimiento duplicado")
                .build();

        ResponseEntity<ResponseModel<IndividualNewsResponseDTO>> response =
                individualNewsController.createDeleteRequest(
                        P_HEADER, CORRELATION_ID, REQUEST_ID, USER, request);

        assertEquals(HttpStatus.CREATED, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals(CODE, response.getBody().getBodyResponse().getCode());
    }

    @Test
    @DisplayName("findPendingNews responde OK con las novedades pendientes")
    void findPendingNewsReturnsOk() {
        when(individualNewsService.findPendingNews(anyString(), anyString(), anyString()))
                .thenReturn(Collections.singletonList(buildNewsResponse(NewsStatus.PENDIENTE)));

        ResponseEntity<ResponseModel<List<IndividualNewsResponseDTO>>> response =
                individualNewsController.findPendingNews(
                        P_HEADER, CORRELATION_ID, REQUEST_ID);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals(1, response.getBody().getBodyResponse().size());
    }

    @Test
    @DisplayName("findPendingNewsByCode responde OK con el detalle de la novedad")
    void findPendingNewsByCodeReturnsOk() {
        when(individualNewsService.findPendingNewsByCode(
                anyString(), anyString(), anyString(), anyLong()))
                .thenReturn(buildNewsResponse(NewsStatus.PENDIENTE));

        ResponseEntity<ResponseModel<IndividualNewsResponseDTO>> response =
                individualNewsController.findPendingNewsByCode(
                        P_HEADER, CORRELATION_ID, REQUEST_ID, CODE);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals(CODE, response.getBody().getBodyResponse().getCode());
    }

    @Test
    @DisplayName("approveNews responde OK con la novedad procesada")
    void approveNewsReturnsOk() {
        when(individualNewsService.approveNews(
                anyString(), anyString(), anyString(), anyString(), anyLong()))
                .thenReturn(buildNewsResponse(NewsStatus.PROCESADO));

        ResponseEntity<ResponseModel<IndividualNewsResponseDTO>> response =
                individualNewsController.approveNews(
                        P_HEADER, CORRELATION_ID, REQUEST_ID, USER, CODE);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals(NewsStatus.PROCESADO.name(),
                response.getBody().getBodyResponse().getStatus());
        verify(individualNewsService).approveNews(
                P_HEADER, CORRELATION_ID, REQUEST_ID, USER, CODE);
    }

    @Test
    @DisplayName("cancelNews responde OK con la novedad cancelada")
    void cancelNewsReturnsOk() {
        when(individualNewsService.cancelNews(
                anyString(), anyString(), anyString(), anyString(), anyLong()))
                .thenReturn(buildNewsResponse(NewsStatus.CANCELADO));

        ResponseEntity<ResponseModel<IndividualNewsResponseDTO>> response =
                individualNewsController.cancelNews(
                        P_HEADER, CORRELATION_ID, REQUEST_ID, USER, CODE);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals(NewsStatus.CANCELADO.name(),
                response.getBody().getBodyResponse().getStatus());
        verify(individualNewsService).cancelNews(
                P_HEADER, CORRELATION_ID, REQUEST_ID, USER, CODE);
    }
}