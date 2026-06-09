package co.com.bnpparibas.cardif.closingclaims.domain.services.impl;

import co.com.bnpparibas.cardif.closingclaims.domain.dtos.homologation.HomologationPolicyRequestDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.homologation.HomologationPolicyResponseDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.entity.HomologationPolicyAlfa;
import co.com.bnpparibas.cardif.closingclaims.domain.util.exception.BusinessException;
import co.com.bnpparibas.cardif.closingclaims.infraestructure.repository.HomologationPolicyAlfaRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.http.HttpStatus;

import java.time.LocalDate;
import java.util.Collections;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class HomologationPolicyAlfaServiceImplTest {

    @Mock
    private HomologationPolicyAlfaRepository repository;

    @InjectMocks
    private HomologationPolicyAlfaServiceImpl service;

    private static final String P_HEADER = "pHeader";
    private static final String CORRELATION_ID = "corr-123";
    private static final String REQUEST_ID = "req-456";

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
    }

    private HomologationPolicyAlfa buildEntity() {
        HomologationPolicyAlfa entity = new HomologationPolicyAlfa();
        entity.setId(1);
        entity.setProducto(749);
        entity.setRamo(31);
        entity.setNroPoliza("0000490");
        entity.setAplicaVigencia(0);
        entity.setFechaInicio(LocalDate.of(2024, 1, 1));
        entity.setFechaFin(LocalDate.of(2024, 12, 31));
        return entity;
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

    @Nested
    @DisplayName("findByProductCode")
    class FindByProductCode {

        @Test
        @DisplayName("returns mapped records")
        void shouldReturnMappedList() {
            when(repository.findByProducto(749))
                    .thenReturn(Collections.singletonList(buildEntity()));

            List<HomologationPolicyResponseDTO> result =
                    service.findByProductCode(P_HEADER, CORRELATION_ID, REQUEST_ID, 749);

            assertEquals(1, result.size());
            assertEquals(749, result.get(0).getProductCode());
            assertEquals("0000490", result.get(0).getPolicyNumber());
            verify(repository, times(1)).findByProducto(749);
        }

        @Test
        @DisplayName("returns empty list when no records exist")
        void shouldReturnEmptyList() {
            when(repository.findByProducto(999))
                    .thenReturn(Collections.emptyList());

            List<HomologationPolicyResponseDTO> result =
                    service.findByProductCode(P_HEADER, CORRELATION_ID, REQUEST_ID, 999);

            assertTrue(result.isEmpty());
        }

        @Test
        @DisplayName("throws BusinessException when repository fails")
        void shouldThrowBusinessExceptionOnRepositoryError() {
            when(repository.findByProducto(any()))
                    .thenThrow(new RuntimeException("DB error"));

            BusinessException exception = assertThrows(
                    BusinessException.class,
                    () -> service.findByProductCode(
                            P_HEADER,
                            CORRELATION_ID,
                            REQUEST_ID,
                            749
                    )
            );

            assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, exception.getHttpStatus());
        }
    }

    @Nested
    @DisplayName("create")
    class Create {

        @Test
        @DisplayName("saves and returns created record")
        void shouldSaveAndReturnDTO() {
            HomologationPolicyAlfa savedEntity = buildEntity();

            when(repository.save(any(HomologationPolicyAlfa.class)))
                    .thenReturn(savedEntity);

            HomologationPolicyResponseDTO result =
                    service.create(P_HEADER, CORRELATION_ID, REQUEST_ID, buildRequest());

            assertNotNull(result);
            assertEquals(749, result.getProductCode());
            assertEquals(1, result.getId());
            verify(repository, times(1))
                    .save(any(HomologationPolicyAlfa.class));
        }

        @Test
        @DisplayName("throws BusinessException when repository fails")
        void shouldThrowBusinessExceptionOnRepositoryError() {
            when(repository.save(any()))
                    .thenThrow(new RuntimeException("DB error"));

            BusinessException exception = assertThrows(
                    BusinessException.class,
                    () -> service.create(
                            P_HEADER,
                            CORRELATION_ID,
                            REQUEST_ID,
                            buildRequest()
                    )
            );

            assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, exception.getHttpStatus());
        }

        @Test
        @DisplayName("throws BAD_REQUEST when start date is after end date")
        void shouldThrowBadRequestWhenDateRangeIsInvalid() {
            HomologationPolicyRequestDTO request = buildRequest();
            request.setStartDate(LocalDate.of(2024, 12, 31));
            request.setEndDate(LocalDate.of(2024, 1, 1));

            BusinessException exception = assertThrows(
                    BusinessException.class,
                    () -> service.create(
                            P_HEADER,
                            CORRELATION_ID,
                            REQUEST_ID,
                            request
                    )
            );

            assertEquals(HttpStatus.BAD_REQUEST, exception.getHttpStatus());
            verify(repository, never()).save(any());
        }
    }

    @Nested
    @DisplayName("update")
    class Update {

        @Test
        @DisplayName("updates and returns edited record")
        void shouldUpdateAndReturnDTO() {
            HomologationPolicyAlfa existingEntity = buildEntity();

            when(repository.findById(1))
                    .thenReturn(Optional.of(existingEntity));

            when(repository.save(any(HomologationPolicyAlfa.class)))
                    .thenReturn(existingEntity);

            HomologationPolicyResponseDTO result =
                    service.update(
                            P_HEADER,
                            CORRELATION_ID,
                            REQUEST_ID,
                            1,
                            buildRequest()
                    );

            assertNotNull(result);
            assertEquals(749, result.getProductCode());
            verify(repository, times(1)).findById(1);
            verify(repository, times(1))
                    .save(any(HomologationPolicyAlfa.class));
        }

        @Test
        @DisplayName("throws NOT_FOUND when id does not exist")
        void shouldThrowNotFoundWhenIdDoesNotExist() {
            when(repository.findById(99))
                    .thenReturn(Optional.empty());

            BusinessException exception = assertThrows(
                    BusinessException.class,
                    () -> service.update(
                            P_HEADER,
                            CORRELATION_ID,
                            REQUEST_ID,
                            99,
                            buildRequest()
                    )
            );

            assertEquals(HttpStatus.NOT_FOUND, exception.getHttpStatus());
        }

        @Test
        @DisplayName("throws BusinessException when repository fails on save")
        void shouldThrowBusinessExceptionOnSaveError() {
            when(repository.findById(1))
                    .thenReturn(Optional.of(buildEntity()));

            when(repository.save(any()))
                    .thenThrow(new RuntimeException("DB error"));

            BusinessException exception = assertThrows(
                    BusinessException.class,
                    () -> service.update(
                            P_HEADER,
                            CORRELATION_ID,
                            REQUEST_ID,
                            1,
                            buildRequest()
                    )
            );

            assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, exception.getHttpStatus());
        }

        @Test
        @DisplayName("throws BAD_REQUEST when start date is after end date")
        void shouldThrowBadRequestWhenDateRangeIsInvalid() {
            HomologationPolicyRequestDTO request = buildRequest();
            request.setStartDate(LocalDate.of(2024, 12, 31));
            request.setEndDate(LocalDate.of(2024, 1, 1));

            BusinessException exception = assertThrows(
                    BusinessException.class,
                    () -> service.update(
                            P_HEADER,
                            CORRELATION_ID,
                            REQUEST_ID,
                            1,
                            request
                    )
            );

            assertEquals(HttpStatus.BAD_REQUEST, exception.getHttpStatus());
            verify(repository, never()).findById(any());
            verify(repository, never()).save(any());
        }
    }

    @Nested
    @DisplayName("delete")
    class Delete {

        @Test
        @DisplayName("deletes record when id exists")
        void shouldDeleteSuccessfully() {
            when(repository.existsById(1)).thenReturn(true);
            doNothing().when(repository).deleteById(1);

            assertDoesNotThrow(
                    () -> service.delete(
                            P_HEADER,
                            CORRELATION_ID,
                            REQUEST_ID,
                            1
                    )
            );

            verify(repository, times(1)).existsById(1);
            verify(repository, times(1)).deleteById(1);
        }

        @Test
        @DisplayName("throws NOT_FOUND when id does not exist")
        void shouldThrowNotFoundWhenIdDoesNotExist() {
            when(repository.existsById(99)).thenReturn(false);

            BusinessException exception = assertThrows(
                    BusinessException.class,
                    () -> service.delete(
                            P_HEADER,
                            CORRELATION_ID,
                            REQUEST_ID,
                            99
                    )
            );

            assertEquals(HttpStatus.NOT_FOUND, exception.getHttpStatus());
            verify(repository, never()).deleteById(any());
        }

        @Test
        @DisplayName("throws BusinessException when repository fails on delete")
        void shouldThrowBusinessExceptionOnDeleteError() {
            when(repository.existsById(1)).thenReturn(true);

            doThrow(new RuntimeException("DB error"))
                    .when(repository)
                    .deleteById(1);

            BusinessException exception = assertThrows(
                    BusinessException.class,
                    () -> service.delete(
                            P_HEADER,
                            CORRELATION_ID,
                            REQUEST_ID,
                            1
                    )
            );

            assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, exception.getHttpStatus());
        }
    }
}
