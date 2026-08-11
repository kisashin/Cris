package co.com.bnpparibas.cardif.closingclaims.domain.util.helpers;

import co.com.bnpparibas.cardif.closingclaims.domain.dtos.individualnews.ClaimMovementResponseDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.individualnews.IndividualNewsRequestDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.individualnews.IndividualNewsResponseDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.entity.ClaimMovementHistory;
import co.com.bnpparibas.cardif.closingclaims.domain.entity.IndividualNewsHistory;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;

import java.util.List;

@Mapper
public interface IndividualNewsMapper {

    IndividualNewsMapper INSTANCE = Mappers.getMapper(IndividualNewsMapper.class);

    /*
     * ClaimMovementHistory -> ClaimMovementResponseDTO
     */
    @Mapping(target = "claimNumber", source = "numeroSiniestro")
    @Mapping(target = "identificationNumber", source = "nroIdentificacion")
    @Mapping(target = "productCode", source = "codProducto")
    @Mapping(target = "planCode", source = "codPlan")
    @Mapping(target = "coverage", source = "cobertura")
    @Mapping(target = "branchCode", source = "ramo")
    @Mapping(target = "movementValue", source = "vrMovimiento")
    @Mapping(target = "movementDate", source = "fechaMovimiento2")
    @Mapping(target = "movementType", source = "tipoMovimiento")
    @Mapping(target = "partner", source = "socio")
    @Mapping(target = "cardifId", source = "idCardif")
    @Mapping(target = "claimKey", source = "llaveSiniestro")
    @Mapping(target = "partnerCode", source = "codSocio")
    @Mapping(target = "claimStatus", source = "estadoSiniestro")
    @Mapping(target = "majorStatus", source = "estadoMayor")
    @Mapping(target = "channel", source = "canal")
    @Mapping(target = "pandemic", source = "pandemia")
    @Mapping(target = "paymentBeneficiary", source = "beneficiarioPago")
    @Mapping(target = "coinsuranceType", source = "tipoCoaseguro")
    @Mapping(target = "retainedCoinsuranceValue", source = "vrCoaseguroRetenido")
    @Mapping(target = "cededCoinsuranceValue", source = "vrCoaseguroCedido")
    @Mapping(target = "birthDate", source = "fechaNacimiento")
    @Mapping(target = "occurrenceDate", source = "fechaOcurrencia")
    @Mapping(target = "partnerNoticeDate", source = "fechaAvisoSocio")
    @Mapping(target = "cardifNoticeDate", source = "fechaAvisoCardif")
    ClaimMovementResponseDTO toMovementResponseDTO(ClaimMovementHistory entity);

    List<ClaimMovementResponseDTO> toMovementResponseDTOList(
            List<ClaimMovementHistory> entities);

    /*
     * IndividualNewsHistory -> IndividualNewsResponseDTO
     */
    @Mapping(target = "code", source = "codigo")
    @Mapping(target = "claimNumber", source = "numeroSiniestro")
    @Mapping(target = "newsType", source = "tipoNovedad")
    @Mapping(target = "status", source = "estado")
    @Mapping(target = "justification", source = "observacion")
    @Mapping(target = "processDate", source = "fechaProceso")
    @Mapping(target = "requestUser", source = "idUsuario")
    @Mapping(target = "authorizerUser", source = "idAutorizador")
    IndividualNewsResponseDTO toNewsResponseDTO(IndividualNewsHistory entity);

    List<IndividualNewsResponseDTO> toNewsResponseDTOList(
            List<IndividualNewsHistory> entities);

    /*
     * IndividualNewsRequestDTO -> IndividualNewsHistory
     */
    @Mapping(target = "codigo", ignore = true)
    @Mapping(target = "estado", ignore = true)
    @Mapping(target = "tipoNovedad", ignore = true)
    @Mapping(target = "fechaProceso", ignore = true)
    @Mapping(target = "idUsuario", ignore = true)
    @Mapping(target = "idAutorizador", ignore = true)
    @Mapping(target = "socio", source = "partner")
    @Mapping(target = "numeroSiniestro", source = "claimNumber")
    @Mapping(target = "fechaNacimiento", source = "birthDate")
    @Mapping(target = "cobertura", source = "coverage")
    @Mapping(target = "ramo", source = "branchCode")
    @Mapping(target = "fechaOcurrencia", source = "occurrenceDate")
    @Mapping(target = "fechaAvisoSocio", source = "partnerNoticeDate")
    @Mapping(target = "fechaAvisoCardif", source = "cardifNoticeDate")
    @Mapping(target = "beneficiarioPago", source = "paymentBeneficiary")
    @Mapping(target = "codSocio", source = "partnerCode")
    @Mapping(target = "idCardif", source = "cardifId")
    @Mapping(target = "llaveSiniestro", source = "claimKey")
    @Mapping(target = "estadoSiniestro", source = "claimStatus")
    @Mapping(target = "estadoMayor", source = "majorStatus")
    @Mapping(target = "tipoMovimiento", source = "movementType")
    @Mapping(target = "canal", source = "channel")
    @Mapping(target = "pandemia", source = "pandemic")
    @Mapping(target = "tipoCoaseguro", source = "coinsuranceType")
    @Mapping(target = "vrCoaseguroRetenido", source = "retainedCoinsuranceValue")
    @Mapping(target = "vrCoaseguroCedido", source = "cededCoinsuranceValue")
    @Mapping(target = "observacion", source = "justification")
    IndividualNewsHistory toEntity(IndividualNewsRequestDTO request);
}