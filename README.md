package co.com.bnpparibas.cardif.closingclaims.domain.services.impl;

import co.com.bnpparibas.cardif.closingclaims.domain.dtos.individualnews.ClaimMovementResponseDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.individualnews.IndividualNewsDeleteRequestDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.individualnews.IndividualNewsRequestDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.individualnews.IndividualNewsResponseDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.entity.ClaimMovementHistory;
import co.com.bnpparibas.cardif.closingclaims.domain.entity.IndividualNewsHistory;
import co.com.bnpparibas.cardif.closingclaims.domain.util.anums.NewsStatus;
import co.com.bnpparibas.cardif.closingclaims.domain.util.anums.NewsType;
import co.com.bnpparibas.cardif.closingclaims.domain.util.exception.BusinessException;
import co.com.bnpparibas.cardif.closingclaims.infraestructure.repository.ClaimMovementHistoryRepository;
import co.com.bnpparibas.cardif.closingclaims.infraestructure.repository.IndividualNewsHistoryRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.HttpStatus;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyLong;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class IndividualNewsServiceImplTest {

    private static final String P_HEADER = "p-header";
    private static final String CORRELATION_ID = "correlation-id";
    private static final String REQUEST_ID = "request-id";
    private static final String CLAIM_NUMBER = "SIN-0001";
    private static final String ANALYST = "f93141";
    private static final String COORDINATOR = "f00999";
    private static final Long ID_CARVAJAL = 100L;
    private static final Long CODE = 55L;

    @Mock
    private ClaimMovementHistoryRepository claimMovementHistoryRepository;

    @Mock
    private IndividualNewsHistoryRepository individualNewsHistoryRepository;

    @InjectMocks
    private IndividualNewsServiceImpl individualNewsService;

    private ClaimMovementHistory movement;
    private IndividualNewsHistory pendingUpdate;

    @BeforeEach
    void setUp() {
        movement = buildMovement();
        pendingUpdate = buildPendingNews(NewsType.ACTUALIZA);
    }

    private ClaimMovementHistory buildMovement() {
        return ClaimMovementHistory.builder()
                .idCarvajal(ID_CARVAJAL)
                .socio("SOCIO ORIGINAL")
                .numeroSiniestro(CLAIM_NUMBER)
                .nroIdentificacion("1020304050")
                .codProducto("2011")
                .codPlan("PLAN-1")
                .cobertura("COBERTURA ORIGINAL")
                .ramo("0001")
                .vrMovimiento(new BigDecimal("1500.50"))
                .fechaMovimiento2(LocalDateTime.of(2026, 5, 10, 0, 0))
                .tipoMovimiento("PAGO")
                .fechaNacimiento(LocalDateTime.of(1980, 1, 1, 0, 0))
                .fechaOcurrencia(LocalDateTime.of(2026, 1, 5, 0, 0))
                .fechaAvisoSocio(LocalDateTime.of(2026, 1, 6, 0, 0))
                .fechaAvisoCardif(LocalDateTime.of(2026, 1, 7, 0, 0))
                .beneficiarioPago("BENEFICIARIO ORIGINAL")
                .codSocio(10)
                .idCardif("IDC-1")
                .llaveSiniestro("LLAVE-1")
                .estadoSiniestro("ABIERTO")
                .estadoMayor("EN ANALISIS")
                .canal("CANAL-1")
                .pandemia("NO")
                .tipoCoaseguro(1)
                .vrCoaseguroRetenido(100.0)
                .vrCoaseguroCedido(50.0)
                .build();
    }

    private IndividualNewsHistory buildPendingNews(NewsType type) {
        return IndividualNewsHistory.builder()
                .codigo(CODE)
                .idCarvajal(ID_CARVAJAL)
                .socio("SOCIO NUEVO")
                .numeroSiniestro(CLAIM_NUMBER)
                .fechaNacimiento(LocalDateTime.of(1981, 2, 2, 0, 0))
                .cobertura("COBERTURA NUEVA")
                .ramo("0002")
                .fechaOcurrencia(LocalDateTime.of(2026, 2, 5, 0, 0))
                .fechaAvisoSocio(LocalDateTime.of(2026, 2, 6, 0, 0))
                .fechaAvisoCardif(LocalDateTime.of(2026, 2, 7, 0, 0))
                .beneficiarioPago("BENEFICIARIO NUEVO")
                .codSocio(20)
                .idCardif("IDC-2")
                .llaveSiniestro("LLAVE-2")
                .estadoSiniestro("CERRADO")
                .estadoMayor("PAGADO")
                .tipoMovimiento("AJUSTE")
                .canal("CANAL-2")
                .pandemia("SI")
                .tipoCoaseguro(2)
                .vrCoaseguroRetenido(200.0)
                .vrCoaseguroCedido(75.0)
                .observacion("Corrige socio")
                .estado(NewsStatus.PENDIENTE)
                .tipoNovedad(type)
                .fechaProceso(LocalDateTime.of(2026, 3, 1, 8, 0))
                .idUsuario(ANALYST)
                .build();
    }

    private IndividualNewsRequestDTO buildUpdateRequest() {
        return IndividualNewsRequestDTO.builder()
                .idCarvajal(ID_CARVAJAL)
                .movementType("AJUSTE")
                .partner("SOCIO NUEVO")
                .coverage("COBERTURA NUEVA")
                .cardifId("IDC-2")
                .claimKey("LLAVE-2")
                .branchCode("0002")
                .claimNumber(CLAIM_NUMBER)
                .partnerCode(20)
                .claimStatus("CERRADO")
                .majorStatus("PAGADO")
                .channel("CANAL-2")
                .pandemic("SI")
                .justification("Corrige socio")
                .paymentBeneficiary("BENEFICIARIO NUEVO")
                .coinsuranceType(2)
                .retainedCoinsuranceValue(200.0)
                .cededCoinsuranceValue(75.0)
                .birthDate(LocalDateTime.of(1981, 2, 2, 0, 0))
                .occurrenceDate(LocalDateTime.of(2026, 2, 5, 0, 0))
                .partnerNoticeDate(LocalDateTime.of(2026, 2, 6, 0, 0))
                .cardifNoticeDate(LocalDateTime.of(2026, 2, 7, 0, 0))
                .build();
    }

    private IndividualNewsDeleteRequestDTO buildDeleteRequest() {
        return IndividualNewsDeleteRequestDTO.builder()
                .idCarvajal(ID_CARVAJAL)
                .justification("Movimiento duplicado")
                .build();
    }

    @Test
    @DisplayName("findMovementsByClaimNumber retorna los movimientos disponibles")
    void findMovementsByClaimNumberReturnsAvailableMovements() {
        when(claimMovementHistoryRepository
                .findAvailableByClaimNumber(CLAIM_NUMBER, NewsStatus.PENDIENTE))
                .thenReturn(Collections.singletonList(movement));

        List<ClaimMovementResponseDTO> result = individualNewsService
                .findMovementsByClaimNumber(P_HEADER, CORRELATION_ID, REQUEST_ID, CLAIM_NUMBER);

        assertEquals(1, result.size());
        assertEquals(ID_CARVAJAL, result.get(0).getIdCarvajal());
        assertEquals(CLAIM_NUMBER, result.get(0).getClaimNumber());
        assertEquals("SOCIO ORIGINAL", result.get(0).getPartner());
        verify(claimMovementHistoryRepository)
                .findAvailableByClaimNumber(CLAIM_NUMBER, NewsStatus.PENDIENTE);
    }

    @Test
    @DisplayName("findMovementsByClaimNumber retorna lista vacia cuando no hay coincidencias")
    void findMovementsByClaimNumberReturnsEmptyList() {
        when(claimMovementHistoryRepository
                .findAvailableByClaimNumber(anyString(), any(NewsStatus.class)))
                .thenReturn(Collections.emptyList());

        List<ClaimMovementResponseDTO> result = individualNewsService
                .findMovementsByClaimNumber(P_HEADER, CORRELATION_ID, REQUEST_ID, CLAIM_NUMBER);

        assertTrue(result.isEmpty());
    }

    @Test
    @DisplayName("findMovementsByClaimNumber envuelve el error de base de datos")
    void findMovementsByClaimNumberWrapsDatabaseError() {
        when(claimMovementHistoryRepository
                .findAvailableByClaimNumber(anyString(), any(NewsStatus.class)))
                .thenThrow(new IllegalStateException("db down"));

        BusinessException exception = assertThrows(BusinessException.class, () ->
                individualNewsService.findMovementsByClaimNumber(
                        P_HEADER, CORRELATION_ID, REQUEST_ID, CLAIM_NUMBER));

        assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, exception.getHttpStatus());
        assertNotNull(exception.getEx());
    }

    @Test
    @DisplayName("findMovementById retorna el movimiento consultado")
    void findMovementByIdReturnsMovement() {
        when(claimMovementHistoryRepository.findById(ID_CARVAJAL))
                .thenReturn(Optional.of(movement));

        ClaimMovementResponseDTO result = individualNewsService
                .findMovementById(P_HEADER, CORRELATION_ID, REQUEST_ID, ID_CARVAJAL);

        assertEquals(ID_CARVAJAL, result.getIdCarvajal());
        assertEquals("IDC-1", result.getCardifId());
        assertEquals(new BigDecimal("1500.50"), result.getMovementValue());
    }

    @Test
    @DisplayName("findMovementById lanza NOT_FOUND cuando el movimiento no existe")
    void findMovementByIdThrowsWhenMovementIsMissing() {
        when(claimMovementHistoryRepository.findById(anyLong()))
                .thenReturn(Optional.empty());

        BusinessException exception = assertThrows(BusinessException.class, () ->
                individualNewsService.findMovementById(
                        P_HEADER, CORRELATION_ID, REQUEST_ID, ID_CARVAJAL));

        assertEquals(HttpStatus.NOT_FOUND, exception.getHttpStatus());
    }

    @Test
    @DisplayName("createUpdateRequest persiste la novedad en estado PENDIENTE")
    void createUpdateRequestSavesPendingNews() {
        when(claimMovementHistoryRepository.existsById(ID_CARVAJAL)).thenReturn(true);
        when(individualNewsHistoryRepository
                .existsByIdCarvajalAndEstado(ID_CARVAJAL, NewsStatus.PENDIENTE))
                .thenReturn(false);
        when(individualNewsHistoryRepository.save(any(IndividualNewsHistory.class)))
                .thenAnswer(invocation -> invocation.getArgument(0));

        IndividualNewsResponseDTO result = individualNewsService.createUpdateRequest(
                P_HEADER, CORRELATION_ID, REQUEST_ID, ANALYST, buildUpdateRequest());

        ArgumentCaptor<IndividualNewsHistory> captor =
                ArgumentCaptor.forClass(IndividualNewsHistory.class);
        verify(individualNewsHistoryRepository).save(captor.capture());

        IndividualNewsHistory saved = captor.getValue();
        assertEquals(NewsStatus.PENDIENTE, saved.getEstado());
        assertEquals(NewsType.ACTUALIZA, saved.getTipoNovedad());
        assertEquals(ANALYST, saved.getIdUsuario());
        assertEquals("SOCIO NUEVO", saved.getSocio());
        assertEquals("Corrige socio", saved.getObservacion());
        assertNotNull(saved.getFechaProceso());
        assertNull(saved.getIdAutorizador());
        assertEquals(NewsStatus.PENDIENTE.name(), result.getStatus());
        assertEquals(NewsType.ACTUALIZA.name(), result.getNewsType());
    }

    @Test
    @DisplayName("createUpdateRequest trunca el usuario a la longitud de la columna")
    void createUpdateRequestTruncatesLongUser() {
        when(claimMovementHistoryRepository.existsById(ID_CARVAJAL)).thenReturn(true);
        when(individualNewsHistoryRepository
                .existsByIdCarvajalAndEstado(ID_CARVAJAL, NewsStatus.PENDIENTE))
                .thenReturn(false);
        when(individualNewsHistoryRepository.save(any(IndividualNewsHistory.class)))
                .thenAnswer(invocation -> invocation.getArgument(0));

        individualNewsService.createUpdateRequest(P_HEADER, CORRELATION_ID, REQUEST_ID,
                "DOMINIO\\usuario.muy.largo.de.prueba", buildUpdateRequest());

        ArgumentCaptor<IndividualNewsHistory> captor =
                ArgumentCaptor.forClass(IndividualNewsHistory.class);
        verify(individualNewsHistoryRepository).save(captor.capture());

        assertEquals(20, captor.getValue().getIdUsuario().length());
    }

    @Test
    @DisplayName("createUpdateRequest deja el usuario nulo cuando llega vacio")
    void createUpdateRequestKeepsNullUserWhenBlank() {
        when(claimMovementHistoryRepository.existsById(ID_CARVAJAL)).thenReturn(true);
        when(individualNewsHistoryRepository
                .existsByIdCarvajalAndEstado(ID_CARVAJAL, NewsStatus.PENDIENTE))
                .thenReturn(false);
        when(individualNewsHistoryRepository.save(any(IndividualNewsHistory.class)))
                .thenAnswer(invocation -> invocation.getArgument(0));

        individualNewsService.createUpdateRequest(P_HEADER, CORRELATION_ID, REQUEST_ID,
                "   ", buildUpdateRequest());

        ArgumentCaptor<IndividualNewsHistory> captor =
                ArgumentCaptor.forClass(IndividualNewsHistory.class);
        verify(individualNewsHistoryRepository).save(captor.capture());

        assertNull(captor.getValue().getIdUsuario());
    }

    @Test
    @DisplayName("createUpdateRequest lanza NOT_FOUND cuando el movimiento no existe")
    void createUpdateRequestThrowsWhenMovementIsMissing() {
        when(claimMovementHistoryRepository.existsById(ID_CARVAJAL)).thenReturn(false);

        IndividualNewsRequestDTO request = buildUpdateRequest();

        BusinessException exception = assertThrows(BusinessException.class, () ->
                individualNewsService.createUpdateRequest(
                        P_HEADER, CORRELATION_ID, REQUEST_ID, ANALYST, request));

        assertEquals(HttpStatus.NOT_FOUND, exception.getHttpStatus());
        verify(individualNewsHistoryRepository, never()).save(any(IndividualNewsHistory.class));
    }

    @Test
    @DisplayName("createUpdateRequest lanza CONFLICT cuando ya existe novedad pendiente")
    void createUpdateRequestThrowsWhenPendingNewsExists() {
        when(claimMovementHistoryRepository.existsById(ID_CARVAJAL)).thenReturn(true);
        when(individualNewsHistoryRepository
                .existsByIdCarvajalAndEstado(ID_CARVAJAL, NewsStatus.PENDIENTE))
                .thenReturn(true);

        IndividualNewsRequestDTO request = buildUpdateRequest();

        BusinessException exception = assertThrows(BusinessException.class, () ->
                individualNewsService.createUpdateRequest(
                        P_HEADER, CORRELATION_ID, REQUEST_ID, ANALYST, request));

        assertEquals(HttpStatus.CONFLICT, exception.getHttpStatus());
        verify(individualNewsHistoryRepository, never()).save(any(IndividualNewsHistory.class));
    }

    @Test
    @DisplayName("createUpdateRequest envuelve el error al persistir")
    void createUpdateRequestWrapsPersistenceError() {
        when(claimMovementHistoryRepository.existsById(ID_CARVAJAL)).thenReturn(true);
        when(individualNewsHistoryRepository
                .existsByIdCarvajalAndEstado(ID_CARVAJAL, NewsStatus.PENDIENTE))
                .thenReturn(false);
        when(individualNewsHistoryRepository.save(any(IndividualNewsHistory.class)))
                .thenThrow(new IllegalStateException("insert failed"));

        IndividualNewsRequestDTO request = buildUpdateRequest();

        BusinessException exception = assertThrows(BusinessException.class, () ->
                individualNewsService.createUpdateRequest(
                        P_HEADER, CORRELATION_ID, REQUEST_ID, ANALYST, request));

        assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, exception.getHttpStatus());
    }

    @Test
    @DisplayName("createDeleteRequest copia los datos de referencia del movimiento")
    void createDeleteRequestCopiesMovementReference() {
        when(claimMovementHistoryRepository.findById(ID_CARVAJAL))
                .thenReturn(Optional.of(movement));
        when(individualNewsHistoryRepository
                .existsByIdCarvajalAndEstado(ID_CARVAJAL, NewsStatus.PENDIENTE))
                .thenReturn(false);
        when(individualNewsHistoryRepository.save(any(IndividualNewsHistory.class)))
                .thenAnswer(invocation -> invocation.getArgument(0));

        IndividualNewsResponseDTO result = individualNewsService.createDeleteRequest(
                P_HEADER, CORRELATION_ID, REQUEST_ID, ANALYST, buildDeleteRequest());

        ArgumentCaptor<IndividualNewsHistory> captor =
                ArgumentCaptor.forClass(IndividualNewsHistory.class);
        verify(individualNewsHistoryRepository).save(captor.capture());

        IndividualNewsHistory saved = captor.getValue();
        assertEquals(NewsType.ELIMINA, saved.getTipoNovedad());
        assertEquals(NewsStatus.PENDIENTE, saved.getEstado());
        assertEquals(CLAIM_NUMBER, saved.getNumeroSiniestro());
        assertEquals("SOCIO ORIGINAL", saved.getSocio());
        assertEquals("Movimiento duplicado", saved.getObservacion());
        assertEquals(ANALYST, saved.getIdUsuario());
        assertEquals(NewsType.ELIMINA.name(), result.getNewsType());
    }

    @Test
    @DisplayName("createDeleteRequest lanza NOT_FOUND cuando el movimiento no existe")
    void createDeleteRequestThrowsWhenMovementIsMissing() {
        when(claimMovementHistoryRepository.findById(ID_CARVAJAL))
                .thenReturn(Optional.empty());

        IndividualNewsDeleteRequestDTO request = buildDeleteRequest();

        BusinessException exception = assertThrows(BusinessException.class, () ->
                individualNewsService.createDeleteRequest(
                        P_HEADER, CORRELATION_ID, REQUEST_ID, ANALYST, request));

        assertEquals(HttpStatus.NOT_FOUND, exception.getHttpStatus());
    }

    @Test
    @DisplayName("createDeleteRequest lanza CONFLICT cuando ya existe novedad pendiente")
    void createDeleteRequestThrowsWhenPendingNewsExists() {
        when(claimMovementHistoryRepository.findById(ID_CARVAJAL))
                .thenReturn(Optional.of(movement));
        when(individualNewsHistoryRepository
                .existsByIdCarvajalAndEstado(ID_CARVAJAL, NewsStatus.PENDIENTE))
                .thenReturn(true);

        IndividualNewsDeleteRequestDTO request = buildDeleteRequest();

        BusinessException exception = assertThrows(BusinessException.class, () ->
                individualNewsService.createDeleteRequest(
                        P_HEADER, CORRELATION_ID, REQUEST_ID, ANALYST, request));

        assertEquals(HttpStatus.CONFLICT, exception.getHttpStatus());
    }

    @Test
    @DisplayName("createDeleteRequest envuelve el error al persistir")
    void createDeleteRequestWrapsPersistenceError() {
        when(claimMovementHistoryRepository.findById(ID_CARVAJAL))
                .thenReturn(Optional.of(movement));
        when(individualNewsHistoryRepository
                .existsByIdCarvajalAndEstado(ID_CARVAJAL, NewsStatus.PENDIENTE))
                .thenReturn(false);
        when(individualNewsHistoryRepository.save(any(IndividualNewsHistory.class)))
                .thenThrow(new IllegalStateException("insert failed"));

        IndividualNewsDeleteRequestDTO request = buildDeleteRequest();

        BusinessException exception = assertThrows(BusinessException.class, () ->
                individualNewsService.createDeleteRequest(
                        P_HEADER, CORRELATION_ID, REQUEST_ID, ANALYST, request));

        assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, exception.getHttpStatus());
    }

    @Test
    @DisplayName("findPendingNews retorna las novedades pendientes")
    void findPendingNewsReturnsPendingRecords() {
        when(individualNewsHistoryRepository
                .findByEstadoOrderByCodigoAsc(NewsStatus.PENDIENTE))
                .thenReturn(Arrays.asList(pendingUpdate, buildPendingNews(NewsType.ELIMINA)));

        List<IndividualNewsResponseDTO> result = individualNewsService
                .findPendingNews(P_HEADER, CORRELATION_ID, REQUEST_ID);

        assertEquals(2, result.size());
        assertEquals(CODE, result.get(0).getCode());
        assertEquals(ANALYST, result.get(0).getRequestUser());
    }

    @Test
    @DisplayName("findPendingNews envuelve el error de base de datos")
    void findPendingNewsWrapsDatabaseError() {
        when(individualNewsHistoryRepository
                .findByEstadoOrderByCodigoAsc(any(NewsStatus.class)))
                .thenThrow(new IllegalStateException("db down"));

        BusinessException exception = assertThrows(BusinessException.class, () ->
                individualNewsService.findPendingNews(P_HEADER, CORRELATION_ID, REQUEST_ID));

        assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, exception.getHttpStatus());
    }

    @Test
    @DisplayName("findPendingNewsByCode retorna el detalle de la novedad")
    void findPendingNewsByCodeReturnsDetail() {
        when(individualNewsHistoryRepository
                .findByCodigoAndEstado(CODE, NewsStatus.PENDIENTE))
                .thenReturn(Optional.of(pendingUpdate));

        IndividualNewsResponseDTO result = individualNewsService
                .findPendingNewsByCode(P_HEADER, CORRELATION_ID, REQUEST_ID, CODE);

        assertEquals(CODE, result.getCode());
        assertEquals("Corrige socio", result.getJustification());
    }

    @Test
    @DisplayName("findPendingNewsByCode lanza CONFLICT cuando la novedad no esta pendiente")
    void findPendingNewsByCodeThrowsWhenNotPending() {
        when(individualNewsHistoryRepository
                .findByCodigoAndEstado(anyLong(), any(NewsStatus.class)))
                .thenReturn(Optional.empty());

        BusinessException exception = assertThrows(BusinessException.class, () ->
                individualNewsService.findPendingNewsByCode(
                        P_HEADER, CORRELATION_ID, REQUEST_ID, CODE));

        assertEquals(HttpStatus.CONFLICT, exception.getHttpStatus());
    }

    @Test
    @DisplayName("approveNews aplica los cambios sobre el movimiento y marca PROCESADO")
    void approveNewsAppliesUpdate() {
        when(individualNewsHistoryRepository
                .findByCodigoAndEstado(CODE, NewsStatus.PENDIENTE))
                .thenReturn(Optional.of(pendingUpdate));
        when(claimMovementHistoryRepository.findById(ID_CARVAJAL))
                .thenReturn(Optional.of(movement));
        when(claimMovementHistoryRepository.save(any(ClaimMovementHistory.class)))
                .thenAnswer(invocation -> invocation.getArgument(0));
        when(individualNewsHistoryRepository.save(any(IndividualNewsHistory.class)))
                .thenAnswer(invocation -> invocation.getArgument(0));

        IndividualNewsResponseDTO result = individualNewsService.approveNews(
                P_HEADER, CORRELATION_ID, REQUEST_ID, COORDINATOR, CODE);

        ArgumentCaptor<ClaimMovementHistory> movementCaptor =
                ArgumentCaptor.forClass(ClaimMovementHistory.class);
        verify(claimMovementHistoryRepository).save(movementCaptor.capture());

        ClaimMovementHistory updated = movementCaptor.getValue();
        assertEquals("SOCIO NUEVO", updated.getSocio());
        assertEquals("COBERTURA NUEVA", updated.getCobertura());
        assertEquals("0002", updated.getRamo());
        assertEquals(Integer.valueOf(20), updated.getCodSocio());
        assertEquals("CERRADO", updated.getEstadoSiniestro());
        assertEquals(Double.valueOf(200.0), updated.getVrCoaseguroRetenido());
        assertEquals(NewsStatus.PROCESADO.name(), result.getStatus());
        assertEquals(COORDINATOR, result.getAuthorizerUser());
        verify(claimMovementHistoryRepository, never()).delete(any(ClaimMovementHistory.class));
    }

    @Test
    @DisplayName("approveNews conserva los campos no gobernados por la novedad")
    void approveNewsKeepsUnmanagedFields() {
        when(individualNewsHistoryRepository
                .findByCodigoAndEstado(CODE, NewsStatus.PENDIENTE))
                .thenReturn(Optional.of(pendingUpdate));
        when(claimMovementHistoryRepository.findById(ID_CARVAJAL))
                .thenReturn(Optional.of(movement));
        when(claimMovementHistoryRepository.save(any(ClaimMovementHistory.class)))
                .thenAnswer(invocation -> invocation.getArgument(0));
        when(individualNewsHistoryRepository.save(any(IndividualNewsHistory.class)))
                .thenAnswer(invocation -> invocation.getArgument(0));

        individualNewsService.approveNews(
                P_HEADER, CORRELATION_ID, REQUEST_ID, COORDINATOR, CODE);

        ArgumentCaptor<ClaimMovementHistory> movementCaptor =
                ArgumentCaptor.forClass(ClaimMovementHistory.class);
        verify(claimMovementHistoryRepository).save(movementCaptor.capture());

        ClaimMovementHistory updated = movementCaptor.getValue();
        assertEquals(new BigDecimal("1500.50"), updated.getVrMovimiento());
        assertEquals("1020304050", updated.getNroIdentificacion());
        assertEquals("2011", updated.getCodProducto());
    }

    @Test
    @DisplayName("approveNews elimina el movimiento cuando la novedad es ELIMINA")
    void approveNewsAppliesDeletion() {
        IndividualNewsHistory pendingDelete = buildPendingNews(NewsType.ELIMINA);

        when(individualNewsHistoryRepository
                .findByCodigoAndEstado(CODE, NewsStatus.PENDIENTE))
                .thenReturn(Optional.of(pendingDelete));
        when(claimMovementHistoryRepository.findById(ID_CARVAJAL))
                .thenReturn(Optional.of(movement));
        when(individualNewsHistoryRepository.save(any(IndividualNewsHistory.class)))
                .thenAnswer(invocation -> invocation.getArgument(0));

        IndividualNewsResponseDTO result = individualNewsService.approveNews(
                P_HEADER, CORRELATION_ID, REQUEST_ID, COORDINATOR, CODE);

        verify(claimMovementHistoryRepository, times(1)).delete(movement);
        verify(claimMovementHistoryRepository, never()).save(any(ClaimMovementHistory.class));
        assertEquals(NewsStatus.PROCESADO.name(), result.getStatus());
    }

    @Test
    @DisplayName("approveNews lanza CONFLICT cuando la novedad ya no esta pendiente")
    void approveNewsThrowsWhenNewsIsNotPending() {
        when(individualNewsHistoryRepository
                .findByCodigoAndEstado(anyLong(), any(NewsStatus.class)))
                .thenReturn(Optional.empty());

        BusinessException exception = assertThrows(BusinessException.class, () ->
                individualNewsService.approveNews(
                        P_HEADER, CORRELATION_ID, REQUEST_ID, COORDINATOR, CODE));

        assertEquals(HttpStatus.CONFLICT, exception.getHttpStatus());
        verify(claimMovementHistoryRepository, never()).findById(anyLong());
    }

    @Test
    @DisplayName("approveNews impide que el solicitante autorice su propia novedad")
    void approveNewsThrowsWhenSameUserApproves() {
        when(individualNewsHistoryRepository
                .findByCodigoAndEstado(CODE, NewsStatus.PENDIENTE))
                .thenReturn(Optional.of(pendingUpdate));

        BusinessException exception = assertThrows(BusinessException.class, () ->
                individualNewsService.approveNews(
                        P_HEADER, CORRELATION_ID, REQUEST_ID, ANALYST, CODE));

        assertEquals(HttpStatus.FORBIDDEN, exception.getHttpStatus());
        verify(claimMovementHistoryRepository, never()).save(any(ClaimMovementHistory.class));
    }

    @Test
    @DisplayName("approveNews permite autorizar cuando la novedad no registra solicitante")
    void approveNewsAllowsWhenRequestUserIsNull() {
        pendingUpdate.setIdUsuario(null);

        when(individualNewsHistoryRepository
                .findByCodigoAndEstado(CODE, NewsStatus.PENDIENTE))
                .thenReturn(Optional.of(pendingUpdate));
        when(claimMovementHistoryRepository.findById(ID_CARVAJAL))
                .thenReturn(Optional.of(movement));
        when(claimMovementHistoryRepository.save(any(ClaimMovementHistory.class)))
                .thenAnswer(invocation -> invocation.getArgument(0));
        when(individualNewsHistoryRepository.save(any(IndividualNewsHistory.class)))
                .thenAnswer(invocation -> invocation.getArgument(0));

        IndividualNewsResponseDTO result = individualNewsService.approveNews(
                P_HEADER, CORRELATION_ID, REQUEST_ID, COORDINATOR, CODE);

        assertEquals(NewsStatus.PROCESADO.name(), result.getStatus());
    }

    @Test
    @DisplayName("approveNews lanza NOT_FOUND cuando el movimiento fue eliminado")
    void approveNewsThrowsWhenMovementIsMissing() {
        when(individualNewsHistoryRepository
                .findByCodigoAndEstado(CODE, NewsStatus.PENDIENTE))
                .thenReturn(Optional.of(pendingUpdate));
        when(claimMovementHistoryRepository.findById(ID_CARVAJAL))
                .thenReturn(Optional.empty());

        BusinessException exception = assertThrows(BusinessException.class, () ->
                individualNewsService.approveNews(
                        P_HEADER, CORRELATION_ID, REQUEST_ID, COORDINATOR, CODE));

        assertEquals(HttpStatus.NOT_FOUND, exception.getHttpStatus());
        verify(individualNewsHistoryRepository, never()).save(any(IndividualNewsHistory.class));
    }

    @Test
    @DisplayName("approveNews envuelve el error al aplicar los cambios")
    void approveNewsWrapsPersistenceError() {
        when(individualNewsHistoryRepository
                .findByCodigoAndEstado(CODE, NewsStatus.PENDIENTE))
                .thenReturn(Optional.of(pendingUpdate));
        when(claimMovementHistoryRepository.findById(ID_CARVAJAL))
                .thenReturn(Optional.of(movement));
        when(claimMovementHistoryRepository.save(any(ClaimMovementHistory.class)))
                .thenThrow(new IllegalStateException("update failed"));

        BusinessException exception = assertThrows(BusinessException.class, () ->
                individualNewsService.approveNews(
                        P_HEADER, CORRELATION_ID, REQUEST_ID, COORDINATOR, CODE));

        assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, exception.getHttpStatus());
    }

    @Test
    @DisplayName("cancelNews marca la novedad como CANCELADO")
    void cancelNewsMarksAsCancelled() {
        when(individualNewsHistoryRepository
                .findByCodigoAndEstado(CODE, NewsStatus.PENDIENTE))
                .thenReturn(Optional.of(pendingUpdate));
        when(individualNewsHistoryRepository.save(any(IndividualNewsHistory.class)))
                .thenAnswer(invocation -> invocation.getArgument(0));

        IndividualNewsResponseDTO result = individualNewsService.cancelNews(
                P_HEADER, CORRELATION_ID, REQUEST_ID, COORDINATOR, CODE);

        assertEquals(NewsStatus.CANCELADO.name(), result.getStatus());
        assertEquals(COORDINATOR, result.getAuthorizerUser());
        verify(claimMovementHistoryRepository, never()).save(any(ClaimMovementHistory.class));
        verify(claimMovementHistoryRepository, never()).delete(any(ClaimMovementHistory.class));
    }

    @Test
    @DisplayName("cancelNews lanza CONFLICT cuando la novedad ya no esta pendiente")
    void cancelNewsThrowsWhenNewsIsNotPending() {
        when(individualNewsHistoryRepository
                .findByCodigoAndEstado(anyLong(), eq(NewsStatus.PENDIENTE)))
                .thenReturn(Optional.empty());

        BusinessException exception = assertThrows(BusinessException.class, () ->
                individualNewsService.cancelNews(
                        P_HEADER, CORRELATION_ID, REQUEST_ID, COORDINATOR, CODE));

        assertEquals(HttpStatus.CONFLICT, exception.getHttpStatus());
    }

    @Test
    @DisplayName("cancelNews envuelve el error al persistir")
    void cancelNewsWrapsPersistenceError() {
        when(individualNewsHistoryRepository
                .findByCodigoAndEstado(CODE, NewsStatus.PENDIENTE))
                .thenReturn(Optional.of(pendingUpdate));
        when(individualNewsHistoryRepository.save(any(IndividualNewsHistory.class)))
                .thenThrow(new IllegalStateException("update failed"));

        BusinessException exception = assertThrows(BusinessException.class, () ->
                individualNewsService.cancelNews(
                        P_HEADER, CORRELATION_ID, REQUEST_ID, COORDINATOR, CODE));

        assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, exception.getHttpStatus());
    }
}