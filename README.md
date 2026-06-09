```java
package co.com.bnpparibas.cardif.closingclaims.domain.services.impl;

import co.com.bnpparibas.cardif.closingclaims.domain.dtos.homologation.HomologationPolicyRequestDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.homologation.HomologationPolicyResponseDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.entity.HomologationPolicyAlfa;
import co.com.bnpparibas.cardif.closingclaims.domain.services.IHomologationPolicyAlfaService;
import co.com.bnpparibas.cardif.closingclaims.domain.util.exception.BusinessException;
import co.com.bnpparibas.cardif.closingclaims.domain.util.helpers.HomologationPolicyAlfaMapper;
import co.com.bnpparibas.cardif.closingclaims.infraestructure.repository.HomologationPolicyAlfaRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
public class HomologationPolicyAlfaServiceImpl
        implements IHomologationPolicyAlfaService {

    private static final Logger logger =
            LoggerFactory.getLogger(HomologationPolicyAlfaServiceImpl.class);

    private final HomologationPolicyAlfaRepository homologationPolicyAlfaRepository;

    public HomologationPolicyAlfaServiceImpl(
            HomologationPolicyAlfaRepository homologationPolicyAlfaRepository) {

        this.homologationPolicyAlfaRepository =
                homologationPolicyAlfaRepository;
    }

    @Override
    @Transactional(readOnly = true)
    public List<HomologationPolicyResponseDTO> findByProductCode(
            String pHeader,
            String correlationId,
            String requestId,
            Integer productCode) {

        try {
            List<HomologationPolicyAlfa> entities =
                    homologationPolicyAlfaRepository.findByProducto(productCode);

            return HomologationPolicyAlfaMapper.INSTANCE
                    .toResponseDTOList(entities);

        } catch (Exception e) {
            logger.error(
                    "Error finding homologations by productCode={}. "
                            + "CorrelationId={}, RequestId={}",
                    productCode,
                    correlationId,
                    requestId,
                    e
            );

            throw new BusinessException(
                    e,
                    null,
                    "Error finding homologations by product code",
                    HttpStatus.INTERNAL_SERVER_ERROR
            );
        }
    }

    @Override
    @Transactional
    public HomologationPolicyResponseDTO create(
            String pHeader,
            String correlationId,
            String requestId,
            HomologationPolicyRequestDTO request) {

        validateDateRange(request);

        try {
            HomologationPolicyAlfa entity =
                    HomologationPolicyAlfaMapper.INSTANCE.toEntity(request);

            HomologationPolicyAlfa savedEntity =
                    homologationPolicyAlfaRepository.save(entity);

            return HomologationPolicyAlfaMapper.INSTANCE
                    .toResponseDTO(savedEntity);

        } catch (Exception e) {
            logger.error(
                    "Error creating homologation. "
                            + "CorrelationId={}, RequestId={}",
                    correlationId,
                    requestId,
                    e
            );

            throw new BusinessException(
                    e,
                    null,
                    "Error creating homologation record",
                    HttpStatus.INTERNAL_SERVER_ERROR
            );
        }
    }

    @Override
    @Transactional
    public HomologationPolicyResponseDTO update(
            String pHeader,
            String correlationId,
            String requestId,
            Integer id,
            HomologationPolicyRequestDTO request) {

        validateDateRange(request);

        HomologationPolicyAlfa entity =
                homologationPolicyAlfaRepository.findById(id)
                        .orElseThrow(() -> new BusinessException(
                                null,
                                "Record not found with id: " + id,
                                HttpStatus.NOT_FOUND
                        ));

        try {
            HomologationPolicyAlfaMapper.INSTANCE
                    .updateEntity(request, entity);

            HomologationPolicyAlfa updatedEntity =
                    homologationPolicyAlfaRepository.save(entity);

            return HomologationPolicyAlfaMapper.INSTANCE
                    .toResponseDTO(updatedEntity);

        } catch (BusinessException e) {
            throw e;

        } catch (Exception e) {
            logger.error(
                    "Error updating homologation id={}. "
                            + "CorrelationId={}, RequestId={}",
                    id,
                    correlationId,
                    requestId,
                    e
            );

            throw new BusinessException(
                    e,
                    null,
                    "Error updating homologation record",
                    HttpStatus.INTERNAL_SERVER_ERROR
            );
        }
    }

    @Override
    @Transactional
    public void delete(
            String pHeader,
            String correlationId,
            String requestId,
            Integer id) {

        if (!homologationPolicyAlfaRepository.existsById(id)) {
            throw new BusinessException(
                    null,
                    "Record not found with id: " + id,
                    HttpStatus.NOT_FOUND
            );
        }

        try {
            homologationPolicyAlfaRepository.deleteById(id);

        } catch (Exception e) {
            logger.error(
                    "Error deleting homologation id={}. "
                            + "CorrelationId={}, RequestId={}",
                    id,
                    correlationId,
                    requestId,
                    e
            );

            throw new BusinessException(
                    e,
                    null,
                    "Error deleting homologation record",
                    HttpStatus.INTERNAL_SERVER_ERROR
            );
        }
    }

    private void validateDateRange(HomologationPolicyRequestDTO request) {
        if (request.getStartDate().isAfter(request.getEndDate())) {
            throw new BusinessException(
                    null,
                    "Start date cannot be greater than end date",
                    HttpStatus.BAD_REQUEST
            );
        }
    }
}
```
