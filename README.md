package co.com.bnpparibas.cardif.closingclaims.domain.services;

import co.com.bnpparibas.cardif.closingclaims.domain.dtos.individualnews.ClaimMovementResponseDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.individualnews.IndividualNewsDeleteRequestDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.individualnews.IndividualNewsRequestDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.individualnews.IndividualNewsResponseDTO;

import java.util.List;

public interface IIndividualNewsService {

    /**
     * Busca los movimientos de un siniestro que no tienen novedad pendiente.
     *
     * @param pHeader       encabezado opcional de seguridad.
     * @param correlationId identificador de correlación.
     * @param requestId     identificador de la petición.
     * @param claimNumber   número de siniestro a consultar.
     * @return lista de movimientos disponibles.
     */
    List<ClaimMovementResponseDTO> findMovementsByClaimNumber(String pHeader,
                                                              String correlationId,
                                                              String requestId,
                                                              String claimNumber);

    /**
     * Obtiene un movimiento por su identificador Carvajal.
     *
     * @param pHeader       encabezado opcional de seguridad.
     * @param correlationId identificador de correlación.
     * @param requestId     identificador de la petición.
     * @param idCarvajal    identificador del movimiento.
     * @return el movimiento consultado.
     */
    ClaimMovementResponseDTO findMovementById(String pHeader, String correlationId,
                                              String requestId, Long idCarvajal);

    /**
     * Registra una solicitud de actualización sobre un movimiento.
     *
     * @param pHeader       encabezado opcional de seguridad.
     * @param correlationId identificador de correlación.
     * @param requestId     identificador de la petición.
     * @param user          usuario que solicita el cambio.
     * @param request       nuevos valores del movimiento.
     * @return la novedad creada.
     */
    IndividualNewsResponseDTO createUpdateRequest(String pHeader, String correlationId,
                                                  String requestId, String user,
                                                  IndividualNewsRequestDTO request);

    /**
     * Registra una solicitud de eliminación sobre un movimiento.
     *
     * @param pHeader       encabezado opcional de seguridad.
     * @param correlationId identificador de correlación.
     * @param requestId     identificador de la petición.
     * @param user          usuario que solicita la eliminación.
     * @param request       identificador y justificación.
     * @return la novedad creada.
     */
    IndividualNewsResponseDTO createDeleteRequest(String pHeader, String correlationId,
                                                  String requestId, String user,
                                                  IndividualNewsDeleteRequestDTO request);

    /**
     * Obtiene las novedades pendientes de autorización.
     *
     * @param pHeader       encabezado opcional de seguridad.
     * @param correlationId identificador de correlación.
     * @param requestId     identificador de la petición.
     * @return lista de novedades pendientes.
     */
    List<IndividualNewsResponseDTO> findPendingNews(String pHeader, String correlationId,
                                                    String requestId);

    /**
     * Obtiene el detalle de una novedad pendiente para su revisión.
     *
     * @param pHeader       encabezado opcional de seguridad.
     * @param correlationId identificador de correlación.
     * @param requestId     identificador de la petición.
     * @param code          identificador de la novedad.
     * @return la novedad consultada.
     */
    IndividualNewsResponseDTO findPendingNewsByCode(String pHeader, String correlationId,
                                                    String requestId, Long code);

    /**
     * Aplica una novedad pendiente sobre el histórico de movimientos.
     *
     * @param pHeader       encabezado opcional de seguridad.
     * @param correlationId identificador de correlación.
     * @param requestId     identificador de la petición.
     * @param user          usuario que autoriza el cambio.
     * @param code          identificador de la novedad.
     * @return la novedad procesada.
     */
    IndividualNewsResponseDTO approveNews(String pHeader, String correlationId,
                                          String requestId, String user, Long code);

    /**
     * Cancela una novedad pendiente.
     *
     * @param pHeader       encabezado opcional de seguridad.
     * @param correlationId identificador de correlación.
     * @param requestId     identificador de la petición.
     * @param user          usuario que cancela la novedad.
     * @param code          identificador de la novedad.
     * @return la novedad cancelada.
     */
    IndividualNewsResponseDTO cancelNews(String pHeader, String correlationId,
                                         String requestId, String user, Long code);
}