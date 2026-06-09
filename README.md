package co.com.bnpparibas.cardif.closingclaims.api;

import co.com.bnpparibas.cardif.closingclaims.domain.dtos.homologation.HomologationPolicyRequestDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.homologation.HomologationPolicyResponseDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.response.model.ResponseModel;
import co.com.bnpparibas.cardif.closingclaims.domain.services.IHomologationPolicyAlfaService;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import java.time.LocalDate;
import java.util.Collections;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class HomologationPolicyAlfaControllerTest {

    @Mock
    private IHomologationPolicyAlfaService service;

    @InjectMocks
    private HomologationPolicyAlfaController controller;

    private static final String P_HEADER = "pHeader";
    private static final String CORRELATION_ID = "corr-123";
    private static final String REQUEST_ID = "req-456";

    private HomologationPolicyResponseDTO buildResponse() {
        return HomologationPolicyResponseDTO.builder()
                .id(1)
                .productCode(749)
                .branchCode(31)
                .policyNumber("0000490")
                .appliesValidity(0)
                .startDate(LocalDate.of(2024, 1, 1))
                .endDate(LocalDate.of(2024, 12, 31))
                .build();
    }

    private HomologationPolicyRequestDTO buildRequest() {
        HomologationPolicyRequestDTO request = new HomologationPolicyRequestDTO();
        request.setProductCode(749);
        request.setBranchCode(31);
        request.setPolicyNumber("0000490");
        request.setAppliesValidity(0);
        request.setStartDate(LocalDate.of(2024, 1, 1));
        request.setEndDate(LocalDate.of(2024, 12, 31));
        return request;
    }

    @Test
    @DisplayName("findByProductCode returns 200 with records")
    void findByProductCode_shouldReturn200WithList() {
        List<HomologationPolicyResponseDTO> list =
                Collections.singletonList(buildResponse());

        when(service.findByProductCode(P_HEADER, CORRELATION_ID, REQUEST_ID, 749))
                .thenReturn(list);

        ResponseEntity<ResponseModel<List<HomologationPolicyResponseDTO>>> response =
                controller.findByProductCode(P_HEADER, CORRELATION_ID, REQUEST_ID, 749);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals(1, response.getBody().getBodyResponse().size());
        assertEquals(CORRELATION_ID, response.getBody().getCorrelationId());

        verify(service, times(1))
                .findByProductCode(P_HEADER, CORRELATION_ID, REQUEST_ID, 749);
    }

    @Test
    @DisplayName("findByProductCode returns an empty list when no records exist")
    void findByProductCode_shouldReturnEmptyList() {
        when(service.findByProductCode(P_HEADER, CORRELATION_ID, REQUEST_ID, 999))
                .thenReturn(Collections.emptyList());

        ResponseEntity<ResponseModel<List<HomologationPolicyResponseDTO>>> response =
                controller.findByProductCode(P_HEADER, CORRELATION_ID, REQUEST_ID, 999);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
        assertTrue(response.getBody().getBodyResponse().isEmpty());
    }

    @Test
    @DisplayName("create returns 201 with the created record")
    void create_shouldReturn201WithCreatedRecord() {
        HomologationPolicyRequestDTO request = buildRequest();
        HomologationPolicyResponseDTO created = buildResponse();

        when(service.create(P_HEADER, CORRELATION_ID, REQUEST_ID, request))
                .thenReturn(created);

        ResponseEntity<ResponseModel<HomologationPolicyResponseDTO>> response =
                controller.create(P_HEADER, CORRELATION_ID, REQUEST_ID, request);

        assertEquals(HttpStatus.CREATED, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals(749, response.getBody().getBodyResponse().getProductCode());

        verify(service, times(1))
                .create(P_HEADER, CORRELATION_ID, REQUEST_ID, request);
    }

    @Test
    @DisplayName("create propagates service exception")
    void create_shouldPropagateServiceException() {
        HomologationPolicyRequestDTO request = buildRequest();

        when(service.create(P_HEADER, CORRELATION_ID, REQUEST_ID, request))
                .thenThrow(new RuntimeException("Error creating record"));

        assertThrows(RuntimeException.class,
                () -> controller.create(P_HEADER, CORRELATION_ID, REQUEST_ID, request));
    }

    @Test
    @DisplayName("update returns 200 with the updated record")
    void update_shouldReturn200WithUpdatedRecord() {
        HomologationPolicyRequestDTO request = buildRequest();
        HomologationPolicyResponseDTO updated = buildResponse();

        when(service.update(P_HEADER, CORRELATION_ID, REQUEST_ID, 1, request))
                .thenReturn(updated);

        ResponseEntity<ResponseModel<HomologationPolicyResponseDTO>> response =
                controller.update(P_HEADER, CORRELATION_ID, REQUEST_ID, 1, request);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals(1, response.getBody().getBodyResponse().getId());

        verify(service, times(1))
                .update(P_HEADER, CORRELATION_ID, REQUEST_ID, 1, request);
    }

    @Test
    @DisplayName("update propagates service exception")
    void update_shouldPropagateServiceException() {
        HomologationPolicyRequestDTO request = buildRequest();

        when(service.update(P_HEADER, CORRELATION_ID, REQUEST_ID, 99, request))
                .thenThrow(new RuntimeException("Record not found"));

        assertThrows(RuntimeException.class,
                () -> controller.update(P_HEADER, CORRELATION_ID, REQUEST_ID, 99, request));
    }

    @Test
    @DisplayName("delete returns 200 with confirmation message")
    void delete_shouldReturn200WithConfirmationMessage() {
        doNothing().when(service)
                .delete(P_HEADER, CORRELATION_ID, REQUEST_ID, 1);

        ResponseEntity<ResponseModel<String>> response =
                controller.delete(P_HEADER, CORRELATION_ID, REQUEST_ID, 1);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals("Record deleted successfully", response.getBody().getBodyResponse());

        verify(service, times(1))
                .delete(P_HEADER, CORRELATION_ID, REQUEST_ID, 1);
    }

    @Test
    @DisplayName("delete propagates service exception")
    void delete_shouldPropagateServiceException() {
        doThrow(new RuntimeException("Record not found"))
                .when(service)
                .delete(P_HEADER, CORRELATION_ID, REQUEST_ID, 99);

        assertThrows(RuntimeException.class,
                () -> controller.delete(P_HEADER, CORRELATION_ID, REQUEST_ID, 99));
    }
}
