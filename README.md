package co.com.bnpparibas.cardif.closingclaims.domain.services;

import co.com.bnpparibas.cardif.closingclaims.domain.dtos.homologation.HomologationPolicyRequestDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.homologation.HomologationPolicyResponseDTO;

import java.util.List;

public interface IHomologationPolicyAlfaService {

    /**
     * Finds policy homologation records by product code.
     *
     * @param pHeader       optional security header.
     * @param correlationId correlation identifier for traceability.
     * @param requestId     request identifier.
     * @param productCode   product code to search.
     * @return list of matching records.
     */
    List<HomologationPolicyResponseDTO> findByProductCode(String pHeader, String correlationId,
                                                          String requestId, Integer productCode);

    /**
     * Creates a new policy homologation record.
     *
     * @param pHeader       optional security header.
     * @param correlationId correlation identifier.
     * @param requestId     request identifier.
     * @param request       data of the record to create.
     * @return created record.
     */
    HomologationPolicyResponseDTO create(String pHeader, String correlationId,
                                         String requestId, HomologationPolicyRequestDTO request);

    /**
     * Updates an existing policy homologation record.
     *
     * @param pHeader       optional security header.
     * @param correlationId correlation identifier.
     * @param requestId     request identifier.
     * @param id            identifier of the record to update.
     * @param request       updated record data.
     * @return updated record.
     */
    HomologationPolicyResponseDTO update(String pHeader, String correlationId,
                                         String requestId, Integer id,
                                         HomologationPolicyRequestDTO request);

    /**
     * Deletes a policy homologation record by its identifier.
     *
     * @param pHeader       optional security header.
     * @param correlationId correlation identifier.
     * @param requestId     request identifier.
     * @param id            identifier of the record to delete.
     */
    void delete(String pHeader, String correlationId, String requestId, Integer id);
}
