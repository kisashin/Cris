package co.com.bnpparibas.cardif.closingclaims.domain.services.impl;

import co.com.bnpparibas.cardif.closingclaims.domain.dtos.individualnews.ClaimMovementResponseDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.individualnews.IndividualNewsDeleteRequestDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.individualnews.IndividualNewsRequestDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.individualnews.IndividualNewsResponseDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.entity.ClaimMovementHistory;
import co.com.bnpparibas.cardif.closingclaims.domain.entity.IndividualNewsHistory;
import co.com.bnpparibas.cardif.closingclaims.domain.services.IIndividualNewsService;
import co.com.bnpparibas.cardif.closingclaims.domain.util.anums.NewsStatus;
import co.com.bnpparibas.cardif.closingclaims.domain.util.anums.NewsType;
import co.com.bnpparibas.cardif.closingclaims.domain.util.exception.BusinessException;
import co.com.bnpparibas.cardif.closingclaims.domain.util.helpers.IndividualNewsMapper;
import co.com.bnpparibas.cardif.closingclaims.domain.util.messages.IndividualNewsMessage;
import co.com.bnpparibas.cardif.closingclaims.infraestructure.repository.ClaimMovementHistoryRepository;
import co.com.bnpparibas.cardif.closingclaims.infraestructure.repository.IndividualNewsHistoryRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;

@Service
public class IndividualNewsServiceImpl implements IIndividualNewsService {

    private static final Logger logger =
            LoggerFactory.getLogger(IndividualNewsServiceImpl.class);

    private static final int USER_MAX_LENGTH = 20;

    private final ClaimMovementHistoryRepository claimMovementHistoryRepository;
    private final IndividualNewsHistoryRepository individualNewsHistoryRepository;

    public IndividualNewsServiceImpl(
            ClaimMovementHistoryRepository claimMovementHistoryRepository,
            IndividualNewsHistoryRepository individualNewsHistoryRepository) {

        this.claimMovementHistoryRepository = claimMovementHistoryRepository;
        this.individualNewsHistoryRepository = individualNewsHistoryRepository;
    }

    @Override
    @Transactional(readOnly = true)
    public List<ClaimMovementResponseDTO> findMovementsByClaimNumber(
            String pHeader,
            String correlationId,
            String requestId,
            String claimNumber) {

        try {
            List<ClaimMovementHistory> movements = claimMovementHistoryRepository
                    .findAvailableByClaimNumber(claimNumber, NewsStatus.PENDIENTE);

            return IndividualNewsMapper.INSTANCE.toMovementResponseDTOList(movements);

        } catch (Exception e) {
            logger.error("Error finding movements by claimNumber={}. "
                            + "CorrelationId={}, RequestId={}",
                    claimNumber, correlationId, requestId, e);

            throw new BusinessException(e, null,
                    IndividualNewsMessage.DATABASE_ACCESS_ERROR.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    @Transactional(readOnly = true)
    public ClaimMovementResponseDTO findMovementById(
            String pHeader,
            String correlationId,
            String requestId,
            Long idCarvajal) {

        ClaimMovementHistory movement = findMovementOrFail(idCarvajal);

        return IndividualNewsMapper.INSTANCE.toMovementResponseDTO(movement);
    }

    @Override
    @Transactional
    public IndividualNewsResponseDTO createUpdateRequest(
            String pHeader,
            String correlationId,
            String requestId,
            String user,
            IndividualNewsRequestDTO request) {

        validateMovementExists(request.getIdCarvajal());
        validateNoPendingNews(request.getIdCarvajal());

        try {
            IndividualNewsHistory entity = IndividualNewsMapper.INSTANCE.toEntity(request);
            entity.setTipoNovedad(NewsType.ACTUALIZA);
            entity.setEstado(NewsStatus.PENDIENTE);
            entity.setFechaProceso(LocalDateTime.now());
            entity.setIdUsuario(truncateUser(user));

            IndividualNewsHistory saved = individualNewsHistoryRepository.save(entity);

            return IndividualNewsMapper.INSTANCE.toNewsResponseDTO(saved);

        } catch (Exception e) {
            logger.error("Error creating update request for idCarvajal={}. "
                            + "CorrelationId={}, RequestId={}",
                    request.getIdCarvajal(), correlationId, requestId, e);

            throw new BusinessException(e, null,
                    IndividualNewsMessage.DATABASE_ACCESS_ERROR.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    @Transactional
    public IndividualNewsResponseDTO createDeleteRequest(
            String pHeader,
            String correlationId,
            String requestId,
            String user,
            IndividualNewsDeleteRequestDTO request) {

        ClaimMovementHistory movement = findMovementOrFail(request.getIdCarvajal());
        validateNoPendingNews(request.getIdCarvajal());

        try {
            IndividualNewsHistory entity = IndividualNewsHistory.builder()
                    .idCarvajal(request.getIdCarvajal())
                    .numeroSiniestro(movement.getNumeroSiniestro())
                    .socio(movement.getSocio())
                    .cobertura(movement.getCobertura())
                    .ramo(movement.getRamo())
                    .tipoMovimiento(movement.getTipoMovimiento())
                    .observacion(request.getJustification())
                    .tipoNovedad(NewsType.ELIMINA)
                    .estado(NewsStatus.PENDIENTE)
                    .fechaProceso(LocalDateTime.now())
                    .idUsuario(truncateUser(user))
                    .build();

            IndividualNewsHistory saved = individualNewsHistoryRepository.save(entity);

            return IndividualNewsMapper.INSTANCE.toNewsResponseDTO(saved);

        } catch (Exception e) {
            logger.error("Error creating delete request for idCarvajal={}. "
                            + "CorrelationId={}, RequestId={}",
                    request.getIdCarvajal(), correlationId, requestId, e);

            throw new BusinessException(e, null,
                    IndividualNewsMessage.DATABASE_ACCESS_ERROR.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    @Transactional(readOnly = true)
    public List<IndividualNewsResponseDTO> findPendingNews(
            String pHeader,
            String correlationId,
            String requestId) {

        try {
            List<IndividualNewsHistory> pending = individualNewsHistoryRepository
                    .findByEstadoOrderByCodigoAsc(NewsStatus.PENDIENTE);

            return IndividualNewsMapper.INSTANCE.toNewsResponseDTOList(pending);

        } catch (Exception e) {
            logger.error("Error finding pending news. CorrelationId={}, RequestId={}",
                    correlationId, requestId, e);

            throw new BusinessException(e, null,
                    IndividualNewsMessage.DATABASE_ACCESS_ERROR.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    @Transactional(readOnly = true)
    public IndividualNewsResponseDTO findPendingNewsByCode(
            String pHeader,
            String correlationId,
            String requestId,
            Long code) {

        IndividualNewsHistory news = findPendingByCode(code);

        return IndividualNewsMapper.INSTANCE.toNewsResponseDTO(news);
    }

    @Override
    @Transactional
    public IndividualNewsResponseDTO approveNews(
            String pHeader,
            String correlationId,
            String requestId,
            String user,
            Long code) {

        IndividualNewsHistory news = findPendingByCode(code);
        validateDifferentUser(news, user);

        ClaimMovementHistory movement = findMovementOrFail(news.getIdCarvajal());

        try {
            if (NewsType.ELIMINA.equals(news.getTipoNovedad())) {
                claimMovementHistoryRepository.delete(movement);
            } else {
                applyChanges(movement, news);
                claimMovementHistoryRepository.save(movement);
            }

            news.setEstado(NewsStatus.PROCESADO);
            news.setIdAutorizador(truncateUser(user));

            IndividualNewsHistory processed = individualNewsHistoryRepository.save(news);

            return IndividualNewsMapper.INSTANCE.toNewsResponseDTO(processed);

        } catch (Exception e) {
            logger.error("Error approving news code={}. CorrelationId={}, RequestId={}",
                    code, correlationId, requestId, e);

            throw new BusinessException(e, null,
                    IndividualNewsMessage.DATABASE_ACCESS_ERROR.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @Override
    @Transactional
    public IndividualNewsResponseDTO cancelNews(
            String pHeader,
            String correlationId,
            String requestId,
            String user,
            Long code) {

        IndividualNewsHistory news = findPendingByCode(code);

        try {
            news.setEstado(NewsStatus.CANCELADO);
            news.setIdAutorizador(truncateUser(user));

            IndividualNewsHistory cancelled = individualNewsHistoryRepository.save(news);

            return IndividualNewsMapper.INSTANCE.toNewsResponseDTO(cancelled);

        } catch (Exception e) {
            logger.error("Error cancelling news code={}. CorrelationId={}, RequestId={}",
                    code, correlationId, requestId, e);

            throw new BusinessException(e, null,
                    IndividualNewsMessage.DATABASE_ACCESS_ERROR.getMessage(),
                    HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    private ClaimMovementHistory findMovementOrFail(Long idCarvajal) {
        return claimMovementHistoryRepository.findById(idCarvajal)
                .orElseThrow(() -> new BusinessException(null,
                        IndividualNewsMessage.MOVEMENT_NOT_FOUND.getMessage(),
                        HttpStatus.NOT_FOUND));
    }

    private IndividualNewsHistory findPendingByCode(Long code) {
        return individualNewsHistoryRepository
                .findByCodigoAndEstado(code, NewsStatus.PENDIENTE)
                .orElseThrow(() -> new BusinessException(null,
                        IndividualNewsMessage.NEWS_NOT_PENDING.getMessage(),
                        HttpStatus.CONFLICT));
    }

    private void validateMovementExists(Long idCarvajal) {
        if (!claimMovementHistoryRepository.existsById(idCarvajal)) {
            throw new BusinessException(null,
                    IndividualNewsMessage.MOVEMENT_NOT_FOUND.getMessage(),
                    HttpStatus.NOT_FOUND);
        }
    }

    private void validateNoPendingNews(Long idCarvajal) {
        if (individualNewsHistoryRepository
                .existsByIdCarvajalAndEstado(idCarvajal, NewsStatus.PENDIENTE)) {
            throw new BusinessException(null,
                    IndividualNewsMessage.PENDING_NEWS_EXISTS.getMessage(),
                    HttpStatus.CONFLICT);
        }
    }

    private void validateDifferentUser(IndividualNewsHistory news, String user) {
        String authorizer = truncateUser(user);
        if (news.getIdUsuario() != null && authorizer != null
                && news.getIdUsuario().equalsIgnoreCase(authorizer)) {
            throw new BusinessException(null,
                    IndividualNewsMessage.SAME_USER_APPROVAL.getMessage(),
                    HttpStatus.FORBIDDEN);
        }
    }

    private void applyChanges(ClaimMovementHistory movement, IndividualNewsHistory news) {
        movement.setSocio(news.getSocio());
        movement.setNumeroSiniestro(news.getNumeroSiniestro());
        movement.setFechaNacimiento(news.getFechaNacimiento());
        movement.setCobertura(news.getCobertura());
        movement.setRamo(news.getRamo());
        movement.setFechaOcurrencia(news.getFechaOcurrencia());
        movement.setFechaAvisoSocio(news.getFechaAvisoSocio());
        movement.setFechaAvisoCardif(news.getFechaAvisoCardif());
        movement.setBeneficiarioPago(news.getBeneficiarioPago());
        movement.setCodSocio(news.getCodSocio());
        movement.setIdCardif(news.getIdCardif());
        movement.setLlaveSiniestro(news.getLlaveSiniestro());
        movement.setEstadoSiniestro(news.getEstadoSiniestro());
        movement.setEstadoMayor(news.getEstadoMayor());
        movement.setTipoMovimiento(news.getTipoMovimiento());
        movement.setCanal(news.getCanal());
        movement.setPandemia(news.getPandemia());
        movement.setTipoCoaseguro(news.getTipoCoaseguro());
        movement.setVrCoaseguroRetenido(news.getVrCoaseguroRetenido());
        movement.setVrCoaseguroCedido(news.getVrCoaseguroCedido());
    }

    private String truncateUser(String user) {
        if (user == null || user.trim().isEmpty()) {
            return null;
        }
        return user.length() > USER_MAX_LENGTH
                ? user.substring(0, USER_MAX_LENGTH) : user;
    }
}