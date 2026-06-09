```java
package co.com.bnpparibas.cardif.closingclaims.api;

import co.com.bnpparibas.cardif.closingclaims.domain.dtos.homologation.HomologationPolicyRequestDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.homologation.HomologationPolicyResponseDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.response.model.ResponseHeader;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.response.model.ResponseModel;
import co.com.bnpparibas.cardif.closingclaims.domain.services.IHomologationPolicyAlfaService;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import java.util.List;

@RestController
@RequestMapping("/v1")
@Tag(name = "Homologación póliza Alfa")
@CrossOrigin("*")
public class HomologationPolicyAlfaController {

    private final IHomologationPolicyAlfaService homologationPolicyAlfaService;

    public HomologationPolicyAlfaController(
            IHomologationPolicyAlfaService homologationPolicyAlfaService) {
        this.homologationPolicyAlfaService = homologationPolicyAlfaService;
    }

    /**
     * Finds policy homologation records by product code.
     *
     * @param pHeader       optional security header.
     * @param correlationId correlation identifier.
     * @param requestId     request identifier.
     * @param productCode   product code to search.
     * @return response containing the matching records.
     */
    @GetMapping("/homologacion-poliza-alfa")
    public ResponseEntity<ResponseModel<List<HomologationPolicyResponseDTO>>> findByProductCode(
            @RequestHeader(value = "_p", required = false) final String pHeader,
            @RequestHeader(value = "correlation_id", required = false) final String correlationId,
            @RequestHeader(value = "request_id", required = false) final String requestId,
            @RequestParam(value = "producto") final Integer productCode) {

        List<HomologationPolicyResponseDTO> result =
                homologationPolicyAlfaService.findByProductCode(
                        pHeader,
                        correlationId,
                        requestId,
                        productCode
                );

        ResponseModel<List<HomologationPolicyResponseDTO>> response =
                new ResponseModel<>(
                        correlationId,
                        ResponseHeader.builder()
                                .returnCode(HttpStatus.OK.value())
                                .build(),
                        result
                );

        return new ResponseEntity<>(response, HttpStatus.OK);
    }

    /**
     * Creates a new policy homologation record.
     *
     * @param pHeader       optional security header.
     * @param correlationId correlation identifier.
     * @param requestId     request identifier.
     * @param request       data of the record to create.
     * @return response containing the created record.
     */
    @PostMapping("/homologacion-poliza-alfa")
    public ResponseEntity<ResponseModel<HomologationPolicyResponseDTO>> create(
            @RequestHeader(value = "_p", required = false) final String pHeader,
            @RequestHeader(value = "correlation_id", required = false) final String correlationId,
            @RequestHeader(value = "request_id", required = false) final String requestId,
            @Valid @RequestBody final HomologationPolicyRequestDTO request) {

        HomologationPolicyResponseDTO created =
                homologationPolicyAlfaService.create(
                        pHeader,
                        correlationId,
                        requestId,
                        request
                );

        ResponseModel<HomologationPolicyResponseDTO> response =
                new ResponseModel<>(
                        correlationId,
                        ResponseHeader.builder()
                                .returnCode(HttpStatus.CREATED.value())
                                .build(),
                        created
                );

        return new ResponseEntity<>(response, HttpStatus.CREATED);
    }

    /**
     * Updates an existing policy homologation record.
     *
     * @param pHeader       optional security header.
     * @param correlationId correlation identifier.
     * @param requestId     request identifier.
     * @param id            record identifier.
     * @param request       updated record data.
     * @return response containing the updated record.
     */
    @PutMapping("/homologacion-poliza-alfa/{id}")
    public ResponseEntity<ResponseModel<HomologationPolicyResponseDTO>> update(
            @RequestHeader(value = "_p", required = false) final String pHeader,
            @RequestHeader(value = "correlation_id", required = false) final String correlationId,
            @RequestHeader(value = "request_id", required = false) final String requestId,
            @PathVariable final Integer id,
            @Valid @RequestBody final HomologationPolicyRequestDTO request) {

        HomologationPolicyResponseDTO updated =
                homologationPolicyAlfaService.update(
                        pHeader,
                        correlationId,
                        requestId,
                        id,
                        request
                );

        ResponseModel<HomologationPolicyResponseDTO> response =
                new ResponseModel<>(
                        correlationId,
                        ResponseHeader.builder()
                                .returnCode(HttpStatus.OK.value())
                                .build(),
                        updated
                );

        return new ResponseEntity<>(response, HttpStatus.OK);
    }

    /**
     * Deletes a policy homologation record by its identifier.
     *
     * @param pHeader       optional security header.
     * @param correlationId correlation identifier.
     * @param requestId     request identifier.
     * @param id            record identifier.
     * @return response containing the deletion confirmation.
     */
    @DeleteMapping("/homologacion-poliza-alfa/{id}")
    public ResponseEntity<ResponseModel<String>> delete(
            @RequestHeader(value = "_p", required = false) final String pHeader,
            @RequestHeader(value = "correlation_id", required = false) final String correlationId,
            @RequestHeader(value = "request_id", required = false) final String requestId,
            @PathVariable final Integer id) {

        homologationPolicyAlfaService.delete(
                pHeader,
                correlationId,
                requestId,
                id
        );

        ResponseModel<String> response =
                new ResponseModel<>(
                        correlationId,
                        ResponseHeader.builder()
                                .returnCode(HttpStatus.OK.value())
                                .build(),
                        "Record deleted successfully"
                );

        return new ResponseEntity<>(response, HttpStatus.OK);
    }
}
```
