import co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia.ColombiaAccountingResultDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia.ColombiaXmlFileDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.entity.ArchivoAsientoCardifXml;


    /**
     * Cuenta los registros de control del cierre de aval.
     */
    @Query(value = "SELECT COUNT(*) FROM controlcierreaval",
            nativeQuery = true)
    int countAvalClosingControl();


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
    ArchivoAsientoCardifXml findXmlFile(
            Integer id, String correlationId, String requestId);
