    /**
     * Ejecuta la generacion de los asientos contables.
     */
    ColombiaAccountingResultDTO generateAccountingEntries(
            String pHeader, String correlationId, String requestId);

    /**
     * Obtiene los archivos XML generados en procesos anteriores.
     */
    List<ColombiaXmlFileDTO> findGeneratedFiles(
            String correlationId, String requestId);

    /**
     * Obtiene un archivo XML persistido.
     */
    ArchivoAsientoAvalXml findXmlFile(
            Integer id, String correlationId, String requestId);



import co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia.ColombiaAccountingResultDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia.ColombiaXmlFileDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.entity.ArchivoAsientoAvalXml;            
