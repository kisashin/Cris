package co.com.bnpparibas.cardif.closingclaims.domain.util.helpers;

import co.com.bnpparibas.cardif.closingclaims.domain.dtos.homologation.HomologationPolicyRequestDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.homologation.HomologationPolicyResponseDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.entity.HomologationPolicyAlfa;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.MappingTarget;
import org.mapstruct.factory.Mappers;

import java.util.List;

@Mapper
public interface HomologationPolicyAlfaMapper {

    HomologationPolicyAlfaMapper INSTANCE =
            Mappers.getMapper(HomologationPolicyAlfaMapper.class);

    /*
     * Entity -> ResponseDTO
     */
    @Mapping(target = "productCode", source = "producto")
    @Mapping(target = "branchCode", source = "ramo")
    @Mapping(target = "policyNumber", source = "nroPoliza")
    @Mapping(target = "appliesValidity", source = "aplicaVigencia")
    @Mapping(target = "startDate", source = "fechaInicio")
    @Mapping(target = "endDate", source = "fechaFin")
    HomologationPolicyResponseDTO toResponseDTO(
            HomologationPolicyAlfa entity
    );

    /*
     * Lista de Entity -> Lista de ResponseDTO
     */
    List<HomologationPolicyResponseDTO> toResponseDTOList(
            List<HomologationPolicyAlfa> entities
    );

    /*
     * RequestDTO -> nueva Entity
     */
    @Mapping(target = "id", ignore = true)
    @Mapping(target = "producto", source = "productCode")
    @Mapping(target = "ramo", source = "branchCode")
    @Mapping(target = "nroPoliza", source = "policyNumber")
    @Mapping(target = "aplicaVigencia", source = "appliesValidity")
    @Mapping(target = "fechaInicio", source = "startDate")
    @Mapping(target = "fechaFin", source = "endDate")
    HomologationPolicyAlfa toEntity(
            HomologationPolicyRequestDTO request
    );

    /*
     * Actualiza una Entity existente sin modificar el ID
     */
    @Mapping(target = "id", ignore = true)
    @Mapping(target = "producto", source = "productCode")
    @Mapping(target = "ramo", source = "branchCode")
    @Mapping(target = "nroPoliza", source = "policyNumber")
    @Mapping(target = "aplicaVigencia", source = "appliesValidity")
    @Mapping(target = "fechaInicio", source = "startDate")
    @Mapping(target = "fechaFin", source = "endDate")
    void updateEntity(
            HomologationPolicyRequestDTO request,
            @MappingTarget HomologationPolicyAlfa entity
    );
}


SERVICE


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
    public List<HomologationPolicyResponseDTO> buscarPorProducto(
            String pHeader,
            String correlationId,
            String requestId,
            Integer producto) {

        try {
            List<HomologationPolicyAlfa> entities =
                    homologationPolicyAlfaRepository.findByProducto(producto);

            return HomologationPolicyAlfaMapper.INSTANCE
                    .toResponseDTOList(entities);

        } catch (Exception e) {
            logger.error(
                    "Error buscando homologaciones por producto={}. "
                            + "CorrelationId={}, RequestId={}",
                    producto,
                    correlationId,
                    requestId,
                    e
            );

            throw new BusinessException(
                    e,
                    null,
                    "Error consultando homologaciones por producto",
                    HttpStatus.INTERNAL_SERVER_ERROR
            );
        }
    }

    @Override
    @Transactional
    public HomologationPolicyResponseDTO crear(
            String pHeader,
            String correlationId,
            String requestId,
            HomologationPolicyRequestDTO request) {

        try {
            HomologationPolicyAlfa entity =
                    HomologationPolicyAlfaMapper.INSTANCE.toEntity(request);

            HomologationPolicyAlfa savedEntity =
                    homologationPolicyAlfaRepository.save(entity);

            return HomologationPolicyAlfaMapper.INSTANCE
                    .toResponseDTO(savedEntity);

        } catch (Exception e) {
            logger.error(
                    "Error creando homologacion. "
                            + "CorrelationId={}, RequestId={}",
                    correlationId,
                    requestId,
                    e
            );

            throw new BusinessException(
                    e,
                    null,
                    "Error creando el registro de homologación",
                    HttpStatus.INTERNAL_SERVER_ERROR
            );
        }
    }

    @Override
    @Transactional
    public HomologationPolicyResponseDTO editar(
            String pHeader,
            String correlationId,
            String requestId,
            Integer id,
            HomologationPolicyRequestDTO request) {

        HomologationPolicyAlfa entity =
                homologationPolicyAlfaRepository.findById(id)
                        .orElseThrow(() -> new BusinessException(
                                null,
                                "Registro no encontrado con id: " + id,
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
                    "Error editando homologacion id={}. "
                            + "CorrelationId={}, RequestId={}",
                    id,
                    correlationId,
                    requestId,
                    e
            );

            throw new BusinessException(
                    e,
                    null,
                    "Error editando el registro de homologación",
                    HttpStatus.INTERNAL_SERVER_ERROR
            );
        }
    }

    @Override
    @Transactional
    public void eliminar(
            String pHeader,
            String correlationId,
            String requestId,
            Integer id) {

        if (!homologationPolicyAlfaRepository.existsById(id)) {
            throw new BusinessException(
                    null,
                    "Registro no encontrado con id: " + id,
                    HttpStatus.NOT_FOUND
            );
        }

        try {
            homologationPolicyAlfaRepository.deleteById(id);

        } catch (Exception e) {
            logger.error(
                    "Error eliminando homologacion id={}. "
                            + "CorrelationId={}, RequestId={}",
                    id,
                    correlationId,
                    requestId,
                    e
            );

            throw new BusinessException(
                    e,
                    null,
                    "Error eliminando el registro de homologación",
                    HttpStatus.INTERNAL_SERVER_ERROR
            );
        }
    }
}
