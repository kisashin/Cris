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

    private static final String P_HEADER       = "pHeader";
    private static final String CORRELATION_ID = "corr-123";
    private static final String REQUEST_ID     = "req-456";

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
    }

    private HomologationPolicyAlfa buildEntity() {
        HomologationPolicyAlfa e = new HomologationPolicyAlfa();
        e.setId(1);
        e.setProducto(749);       // entity mantiene español — va a BD
        e.setRamo(31);
        e.setNroPoliza("0000490");
        e.setAplicaVigencia(0);
        e.setFechaInicio(LocalDate.of(2024, 1, 1));
        e.setFechaFin(LocalDate.of(2024, 12, 31));
        return e;
    }

    private HomologationPolicyRequestDTO buildRequest() {
        HomologationPolicyRequestDTO req = new HomologationPolicyRequestDTO();
        req.setProductCode(749);
        req.setBranchCode(31);
        req.setPolicyNumber("0000490");
        req.setAppliesValidity(0);
        req.setStartDate(LocalDate.of(2024, 1, 1));
        req.setEndDate(LocalDate.of(2024, 12, 31));
        return req;
    }

    /* ------------------------------------------------------------------ */
    @Nested
    @DisplayName("buscarPorProducto")
    class BuscarPorProducto {

        @Test
        @DisplayName("retorna lista mapeada correctamente")
        void shouldReturnMappedList() {
            when(repository.findByProducto(749))
                    .thenReturn(Collections.singletonList(buildEntity()));

            List<HomologationPolicyResponseDTO> result =
                    service.buscarPorProducto(P_HEADER, CORRELATION_ID, REQUEST_ID, 749);

            assertEquals(1, result.size());
            assertEquals(749, result.get(0).getProductCode());
            assertEquals("0000490", result.get(0).getPolicyNumber());
            verify(repository, times(1)).findByProducto(749);
        }

        @Test
        @DisplayName("retorna lista vacía cuando no hay registros")
        void shouldReturnEmptyList() {
            when(repository.findByProducto(999)).thenReturn(Collections.emptyList());

            List<HomologationPolicyResponseDTO> result =
                    service.buscarPorProducto(P_HEADER, CORRELATION_ID, REQUEST_ID, 999);

            assertTrue(result.isEmpty());
        }

        @Test
        @DisplayName("lanza BusinessException cuando el repositorio falla")
        void shouldThrowBusinessExceptionOnRepositoryError() {
            when(repository.findByProducto(any()))
                    .thenThrow(new RuntimeException("DB error"));

            BusinessException ex = assertThrows(BusinessException.class,
                    () -> service.buscarPorProducto(P_HEADER, CORRELATION_ID, REQUEST_ID, 749));

            assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, ex.getHttpStatus());
        }
    }

    /* ------------------------------------------------------------------ */
    @Nested
    @DisplayName("crear")
    class Crear {

        @Test
        @DisplayName("guarda y retorna el DTO creado")
        void shouldSaveAndReturnDTO() {
            HomologationPolicyAlfa saved = buildEntity();
            when(repository.save(any(HomologationPolicyAlfa.class))).thenReturn(saved);

            HomologationPolicyResponseDTO result =
                    service.crear(P_HEADER, CORRELATION_ID, REQUEST_ID, buildRequest());

            assertNotNull(result);
            assertEquals(749, result.getProductCode());
            assertEquals(1, result.getId());
            verify(repository, times(1)).save(any(HomologationPolicyAlfa.class));
        }

        @Test
        @DisplayName("lanza BusinessException cuando el repositorio falla")
        void shouldThrowBusinessExceptionOnRepositoryError() {
            when(repository.save(any())).thenThrow(new RuntimeException("DB error"));

            BusinessException ex = assertThrows(BusinessException.class,
                    () -> service.crear(P_HEADER, CORRELATION_ID, REQUEST_ID, buildRequest()));

            assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, ex.getHttpStatus());
        }
    }

    /* ------------------------------------------------------------------ */
    @Nested
    @DisplayName("editar")
    class Editar {

        @Test
        @DisplayName("actualiza y retorna el DTO editado")
        void shouldUpdateAndReturnDTO() {
            HomologationPolicyAlfa existing = buildEntity();
            when(repository.findById(1)).thenReturn(Optional.of(existing));
            when(repository.save(any(HomologationPolicyAlfa.class))).thenReturn(existing);

            HomologationPolicyResponseDTO result =
                    service.editar(P_HEADER, CORRELATION_ID, REQUEST_ID, 1, buildRequest());

            assertNotNull(result);
            assertEquals(749, result.getProductCode());
            verify(repository, times(1)).findById(1);
            verify(repository, times(1)).save(any(HomologationPolicyAlfa.class));
        }

        @Test
        @DisplayName("lanza BusinessException con NOT_FOUND cuando el id no existe")
        void shouldThrowNotFoundWhenIdDoesNotExist() {
            when(repository.findById(99)).thenReturn(Optional.empty());

            BusinessException ex = assertThrows(BusinessException.class,
                    () -> service.editar(P_HEADER, CORRELATION_ID, REQUEST_ID, 99, buildRequest()));

            assertEquals(HttpStatus.NOT_FOUND, ex.getHttpStatus());
        }

        @Test
        @DisplayName("lanza BusinessException cuando el repositorio falla al guardar")
        void shouldThrowBusinessExceptionOnSaveError() {
            when(repository.findById(1)).thenReturn(Optional.of(buildEntity()));
            when(repository.save(any())).thenThrow(new RuntimeException("DB error"));

            BusinessException ex = assertThrows(BusinessException.class,
                    () -> service.editar(P_HEADER, CORRELATION_ID, REQUEST_ID, 1, buildRequest()));

            assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, ex.getHttpStatus());
        }
    }

    /* ------------------------------------------------------------------ */
    @Nested
    @DisplayName("eliminar")
    class Eliminar {

        @Test
        @DisplayName("elimina correctamente cuando el id existe")
        void shouldDeleteSuccessfully() {
            when(repository.existsById(1)).thenReturn(true);
            doNothing().when(repository).deleteById(1);

            assertDoesNotThrow(
                    () -> service.eliminar(P_HEADER, CORRELATION_ID, REQUEST_ID, 1));

            verify(repository, times(1)).existsById(1);
            verify(repository, times(1)).deleteById(1);
        }

        @Test
        @DisplayName("lanza BusinessException con NOT_FOUND cuando el id no existe")
        void shouldThrowNotFoundWhenIdDoesNotExist() {
            when(repository.existsById(99)).thenReturn(false);

            BusinessException ex = assertThrows(BusinessException.class,
                    () -> service.eliminar(P_HEADER, CORRELATION_ID, REQUEST_ID, 99));

            assertEquals(HttpStatus.NOT_FOUND, ex.getHttpStatus());
            verify(repository, never()).deleteById(any());
        }

        @Test
        @DisplayName("lanza BusinessException cuando el repositorio falla al eliminar")
        void shouldThrowBusinessExceptionOnDeleteError() {
            when(repository.existsById(1)).thenReturn(true);
            doThrow(new RuntimeException("DB error")).when(repository).deleteById(1);

            BusinessException ex = assertThrows(BusinessException.class,
                    () -> service.eliminar(P_HEADER, CORRELATION_ID, REQUEST_ID, 1));

            assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, ex.getHttpStatus());
        }
    }
}
