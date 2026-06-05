Dónde va cada archivo:
src/test/java/co/com/bnpparibas/cardif/closingclaims/

  domain/entity/
    HomologaPolizaAlfaTest.java          ← Entity (3 tests)

  domain/dtos/homologa/
    HomologaPolizaDTOsTest.java          ← Request y Response DTOs (6 tests)

  domain/services/impl/
    HomologaPolizaAlfaServiceImplTest.java ← Service (11 tests)

  api/
    HomologaPolizaAlfaControllerTest.java  ← Controller (8 tests)
Total: 28 tests distribuidos así:

Entity → getters, setters, campos nulos
DTOs → constructores, builders, setters
Service → happy path y errores para los 4 métodos con @Nested
Controller → 200/201 esperados, propagación de excepciones

Con eso deberías superar el 90% de cobertura en JaCoCo. Ejecuta mvn test y si algún test falla por diferencia en tipos o nombres de métodos, pégame el error y lo ajusto.



HomologaPolizaAlfaControllerTest

package co.com.bnpparibas.cardif.closingclaims.api;

import co.com.bnpparibas.cardif.closingclaims.domain.dtos.homologa.HomologaPolizaRequestDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.homologa.HomologaPolizaResponseDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.response.model.ResponseModel;
import co.com.bnpparibas.cardif.closingclaims.domain.services.IHomologaPolizaAlfaService;
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
class HomologaPolizaAlfaControllerTest {

    @Mock
    private IHomologaPolizaAlfaService service;

    @InjectMocks
    private HomologaPolizaAlfaController controller;

    private static final String P_HEADER      = "pHeader";
    private static final String CORRELATION_ID = "corr-123";
    private static final String REQUEST_ID     = "req-456";

    private HomologaPolizaResponseDTO buildResponse() {
        return HomologaPolizaResponseDTO.builder()
                .id(1)
                .producto(749)
                .ramo(31)
                .nroPoliza("0000490")
                .aplicaVigencia(0)
                .fechaInicio(LocalDate.of(2024, 1, 1))
                .fechaFin(LocalDate.of(2024, 12, 31))
                .build();
    }

    private HomologaPolizaRequestDTO buildRequest() {
        HomologaPolizaRequestDTO req = new HomologaPolizaRequestDTO();
        req.setProducto(749);
        req.setRamo(31);
        req.setNroPoliza("0000490");
        req.setAplicaVigencia(0);
        req.setFechaInicio(LocalDate.of(2024, 1, 1));
        req.setFechaFin(LocalDate.of(2024, 12, 31));
        return req;
    }

    @Test
    @DisplayName("buscarPorProducto retorna 200 con lista de registros")
    void buscarPorProducto_shouldReturn200WithList() {
        List<HomologaPolizaResponseDTO> lista = Collections.singletonList(buildResponse());
        when(service.buscarPorProducto(P_HEADER, CORRELATION_ID, REQUEST_ID, 749))
                .thenReturn(lista);

        ResponseEntity<ResponseModel<List<HomologaPolizaResponseDTO>>> response =
                controller.buscarPorProducto(P_HEADER, CORRELATION_ID, REQUEST_ID, 749);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals(1, response.getBody().getBodyResponse().size());
        assertEquals(CORRELATION_ID, response.getBody().getCorrelationId());
        verify(service, times(1))
                .buscarPorProducto(P_HEADER, CORRELATION_ID, REQUEST_ID, 749);
    }

    @Test
    @DisplayName("buscarPorProducto retorna lista vacía cuando no hay registros")
    void buscarPorProducto_shouldReturnEmptyList() {
        when(service.buscarPorProducto(P_HEADER, CORRELATION_ID, REQUEST_ID, 999))
                .thenReturn(Collections.emptyList());

        ResponseEntity<ResponseModel<List<HomologaPolizaResponseDTO>>> response =
                controller.buscarPorProducto(P_HEADER, CORRELATION_ID, REQUEST_ID, 999);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
        assertTrue(response.getBody().getBodyResponse().isEmpty());
    }

    @Test
    @DisplayName("crear retorna 201 con el registro creado")
    void crear_shouldReturn201WithCreatedRecord() {
        HomologaPolizaRequestDTO request  = buildRequest();
        HomologaPolizaResponseDTO created = buildResponse();
        when(service.crear(P_HEADER, CORRELATION_ID, REQUEST_ID, request))
                .thenReturn(created);

        ResponseEntity<ResponseModel<HomologaPolizaResponseDTO>> response =
                controller.crear(P_HEADER, CORRELATION_ID, REQUEST_ID, request);

        assertEquals(HttpStatus.CREATED, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals(749, response.getBody().getBodyResponse().getProducto());
        verify(service, times(1))
                .crear(P_HEADER, CORRELATION_ID, REQUEST_ID, request);
    }

    @Test
    @DisplayName("crear propaga excepción del servicio")
    void crear_shouldPropagateServiceException() {
        HomologaPolizaRequestDTO request = buildRequest();
        when(service.crear(P_HEADER, CORRELATION_ID, REQUEST_ID, request))
                .thenThrow(new RuntimeException("Error al crear"));

        assertThrows(RuntimeException.class,
                () -> controller.crear(P_HEADER, CORRELATION_ID, REQUEST_ID, request));
    }

    @Test
    @DisplayName("editar retorna 200 con el registro actualizado")
    void editar_shouldReturn200WithUpdatedRecord() {
        HomologaPolizaRequestDTO request  = buildRequest();
        HomologaPolizaResponseDTO updated = buildResponse();
        when(service.editar(P_HEADER, CORRELATION_ID, REQUEST_ID, 1, request))
                .thenReturn(updated);

        ResponseEntity<ResponseModel<HomologaPolizaResponseDTO>> response =
                controller.editar(P_HEADER, CORRELATION_ID, REQUEST_ID, 1, request);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals(1, response.getBody().getBodyResponse().getId());
        verify(service, times(1))
                .editar(P_HEADER, CORRELATION_ID, REQUEST_ID, 1, request);
    }

    @Test
    @DisplayName("editar propaga excepción del servicio")
    void editar_shouldPropagateServiceException() {
        HomologaPolizaRequestDTO request = buildRequest();
        when(service.editar(P_HEADER, CORRELATION_ID, REQUEST_ID, 99, request))
                .thenThrow(new RuntimeException("No encontrado"));

        assertThrows(RuntimeException.class,
                () -> controller.editar(P_HEADER, CORRELATION_ID, REQUEST_ID, 99, request));
    }

    @Test
    @DisplayName("eliminar retorna 200 con mensaje de confirmación")
    void eliminar_shouldReturn200WithConfirmationMessage() {
        doNothing().when(service).eliminar(P_HEADER, CORRELATION_ID, REQUEST_ID, 1);

        ResponseEntity<ResponseModel<String>> response =
                controller.eliminar(P_HEADER, CORRELATION_ID, REQUEST_ID, 1);

        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertNotNull(response.getBody());
        assertEquals("Registro eliminado con éxito", response.getBody().getBodyResponse());
        verify(service, times(1))
                .eliminar(P_HEADER, CORRELATION_ID, REQUEST_ID, 1);
    }

    @Test
    @DisplayName("eliminar propaga excepción del servicio")
    void eliminar_shouldPropagateServiceException() {
        doThrow(new RuntimeException("No encontrado"))
                .when(service).eliminar(P_HEADER, CORRELATION_ID, REQUEST_ID, 99);

        assertThrows(RuntimeException.class,
                () -> controller.eliminar(P_HEADER, CORRELATION_ID, REQUEST_ID, 99));
    }
}


HomologaPolizaAlfaServiceImplTest


package co.com.bnpparibas.cardif.closingclaims.domain.services.impl;

import co.com.bnpparibas.cardif.closingclaims.domain.dtos.homologa.HomologaPolizaRequestDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.homologa.HomologaPolizaResponseDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.entity.HomologaPolizaAlfa;
import co.com.bnpparibas.cardif.closingclaims.domain.util.exception.BusinessException;
import co.com.bnpparibas.cardif.closingclaims.infraestructure.repository.HomologaPolizaAlfaRepository;
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

class HomologaPolizaAlfaServiceImplTest {

    @Mock
    private HomologaPolizaAlfaRepository repository;

    @InjectMocks
    private HomologaPolizaAlfaServiceImpl service;

    private static final String P_HEADER      = "pHeader";
    private static final String CORRELATION_ID = "corr-123";
    private static final String REQUEST_ID     = "req-456";

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
    }

    private HomologaPolizaAlfa buildEntity() {
        HomologaPolizaAlfa e = new HomologaPolizaAlfa();
        e.setId(1);
        e.setProducto(749);
        e.setRamo(31);
        e.setNroPoliza("0000490");
        e.setAplicaVigencia(0);
        e.setFechaInicio(LocalDate.of(2024, 1, 1));
        e.setFechaFin(LocalDate.of(2024, 12, 31));
        return e;
    }

    private HomologaPolizaRequestDTO buildRequest() {
        HomologaPolizaRequestDTO req = new HomologaPolizaRequestDTO();
        req.setProducto(749);
        req.setRamo(31);
        req.setNroPoliza("0000490");
        req.setAplicaVigencia(0);
        req.setFechaInicio(LocalDate.of(2024, 1, 1));
        req.setFechaFin(LocalDate.of(2024, 12, 31));
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

            List<HomologaPolizaResponseDTO> result =
                    service.buscarPorProducto(P_HEADER, CORRELATION_ID, REQUEST_ID, 749);

            assertEquals(1, result.size());
            assertEquals(749, result.get(0).getProducto());
            assertEquals("0000490", result.get(0).getNroPoliza());
            verify(repository, times(1)).findByProducto(749);
        }

        @Test
        @DisplayName("retorna lista vacía cuando no hay registros")
        void shouldReturnEmptyList() {
            when(repository.findByProducto(999)).thenReturn(Collections.emptyList());

            List<HomologaPolizaResponseDTO> result =
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
            HomologaPolizaAlfa saved = buildEntity();
            when(repository.save(any(HomologaPolizaAlfa.class))).thenReturn(saved);

            HomologaPolizaResponseDTO result =
                    service.crear(P_HEADER, CORRELATION_ID, REQUEST_ID, buildRequest());

            assertNotNull(result);
            assertEquals(749, result.getProducto());
            assertEquals(1, result.getId());
            verify(repository, times(1)).save(any(HomologaPolizaAlfa.class));
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
            HomologaPolizaAlfa existing = buildEntity();
            when(repository.findById(1)).thenReturn(Optional.of(existing));
            when(repository.save(any(HomologaPolizaAlfa.class))).thenReturn(existing);

            HomologaPolizaResponseDTO result =
                    service.editar(P_HEADER, CORRELATION_ID, REQUEST_ID, 1, buildRequest());

            assertNotNull(result);
            assertEquals(749, result.getProducto());
            verify(repository, times(1)).findById(1);
            verify(repository, times(1)).save(any(HomologaPolizaAlfa.class));
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

HomologaPolizaAlfaTest


package co.com.bnpparibas.cardif.closingclaims.domain.entity;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;

import java.time.LocalDate;

import static org.junit.jupiter.api.Assertions.*;

@ExtendWith(MockitoExtension.class)
class HomologaPolizaAlfaTest {

    @Test
    @DisplayName("Constructor con todos los argumentos asigna los valores correctamente")
    void allArgsConstructor_shouldSetAllFields() {
        LocalDate fechaInicio = LocalDate.of(2024, 1, 1);
        LocalDate fechaFin    = LocalDate.of(2024, 12, 31);

        HomologaPolizaAlfa entity = new HomologaPolizaAlfa(
                1, 749, 31, "0000490", 0, fechaInicio, fechaFin
        );

        assertAll(
                () -> assertEquals(1,          entity.getId()),
                () -> assertEquals(749,        entity.getProducto()),
                () -> assertEquals(31,         entity.getRamo()),
                () -> assertEquals("0000490",  entity.getNroPoliza()),
                () -> assertEquals(0,          entity.getAplicaVigencia()),
                () -> assertEquals(fechaInicio, entity.getFechaInicio()),
                () -> assertEquals(fechaFin,    entity.getFechaFin())
        );
    }

    @Test
    @DisplayName("Constructor sin argumentos + setters asignan los valores correctamente")
    void noArgsConstructorAndSetters_shouldSetAllFields() {
        LocalDate fechaInicio = LocalDate.of(2024, 1, 1);
        LocalDate fechaFin    = LocalDate.of(2024, 12, 31);

        HomologaPolizaAlfa entity = new HomologaPolizaAlfa();
        entity.setId(2);
        entity.setProducto(1001);
        entity.setRamo(24);
        entity.setNroPoliza("0000001");
        entity.setAplicaVigencia(1);
        entity.setFechaInicio(fechaInicio);
        entity.setFechaFin(fechaFin);

        assertAll(
                () -> assertEquals(2,          entity.getId()),
                () -> assertEquals(1001,       entity.getProducto()),
                () -> assertEquals(24,         entity.getRamo()),
                () -> assertEquals("0000001",  entity.getNroPoliza()),
                () -> assertEquals(1,          entity.getAplicaVigencia()),
                () -> assertEquals(fechaInicio, entity.getFechaInicio()),
                () -> assertEquals(fechaFin,    entity.getFechaFin())
        );
    }

    @Test
    @DisplayName("Campos opcionales pueden ser nulos")
    void optionalFields_canBeNull() {
        HomologaPolizaAlfa entity = new HomologaPolizaAlfa();
        assertNull(entity.getFechaInicio());
        assertNull(entity.getFechaFin());
        assertNull(entity.getAplicaVigencia());
    }
}

HomologaPolizaDTOsTest


package co.com.bnpparibas.cardif.closingclaims.domain.dtos.homologa;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;

import java.time.LocalDate;

import static org.junit.jupiter.api.Assertions.*;

@ExtendWith(MockitoExtension.class)
class HomologaPolizaDTOsTest {

    private static final LocalDate FECHA_INICIO = LocalDate.of(2024, 1, 1);
    private static final LocalDate FECHA_FIN    = LocalDate.of(2024, 12, 31);

    /* ------------------------------------------------------------------ */
    @Test
    @DisplayName("HomologaPolizaRequestDTO - constructor sin args + setters")
    void requestDTO_noArgsAndSetters() {
        HomologaPolizaRequestDTO dto = new HomologaPolizaRequestDTO();
        dto.setProducto(749);
        dto.setRamo(31);
        dto.setNroPoliza("0000490");
        dto.setAplicaVigencia(0);
        dto.setFechaInicio(FECHA_INICIO);
        dto.setFechaFin(FECHA_FIN);

        assertAll(
                () -> assertEquals(749,        dto.getProducto()),
                () -> assertEquals(31,         dto.getRamo()),
                () -> assertEquals("0000490",  dto.getNroPoliza()),
                () -> assertEquals(0,          dto.getAplicaVigencia()),
                () -> assertEquals(FECHA_INICIO, dto.getFechaInicio()),
                () -> assertEquals(FECHA_FIN,    dto.getFechaFin())
        );
    }

    @Test
    @DisplayName("HomologaPolizaRequestDTO - constructor con todos los args")
    void requestDTO_allArgsConstructor() {
        HomologaPolizaRequestDTO dto = new HomologaPolizaRequestDTO(
                749, 31, "0000490", 0, FECHA_INICIO, FECHA_FIN
        );

        assertAll(
                () -> assertEquals(749,        dto.getProducto()),
                () -> assertEquals(31,         dto.getRamo()),
                () -> assertEquals("0000490",  dto.getNroPoliza()),
                () -> assertEquals(FECHA_INICIO, dto.getFechaInicio()),
                () -> assertEquals(FECHA_FIN,    dto.getFechaFin())
        );
    }

    @Test
    @DisplayName("HomologaPolizaRequestDTO - fechas opcionales pueden ser nulas")
    void requestDTO_nullDates() {
        HomologaPolizaRequestDTO dto = new HomologaPolizaRequestDTO();
        dto.setProducto(749);
        assertNull(dto.getFechaInicio());
        assertNull(dto.getFechaFin());
    }

    /* ------------------------------------------------------------------ */
    @Test
    @DisplayName("HomologaPolizaResponseDTO - builder asigna todos los campos")
    void responseDTO_builderSetsAllFields() {
        HomologaPolizaResponseDTO dto = HomologaPolizaResponseDTO.builder()
                .id(1)
                .producto(749)
                .ramo(31)
                .nroPoliza("0000490")
                .aplicaVigencia(0)
                .fechaInicio(FECHA_INICIO)
                .fechaFin(FECHA_FIN)
                .build();

        assertAll(
                () -> assertEquals(1,          dto.getId()),
                () -> assertEquals(749,        dto.getProducto()),
                () -> assertEquals(31,         dto.getRamo()),
                () -> assertEquals("0000490",  dto.getNroPoliza()),
                () -> assertEquals(0,          dto.getAplicaVigencia()),
                () -> assertEquals(FECHA_INICIO, dto.getFechaInicio()),
                () -> assertEquals(FECHA_FIN,    dto.getFechaFin())
        );
    }

    @Test
    @DisplayName("HomologaPolizaResponseDTO - constructor sin args + setters")
    void responseDTO_noArgsAndSetters() {
        HomologaPolizaResponseDTO dto = new HomologaPolizaResponseDTO();
        dto.setId(2);
        dto.setProducto(1001);
        dto.setRamo(24);
        dto.setNroPoliza("0000001");
        dto.setAplicaVigencia(1);
        dto.setFechaInicio(FECHA_INICIO);
        dto.setFechaFin(FECHA_FIN);

        assertAll(
                () -> assertEquals(2,          dto.getId()),
                () -> assertEquals(1001,       dto.getProducto()),
                () -> assertEquals(24,         dto.getRamo()),
                () -> assertEquals("0000001",  dto.getNroPoliza()),
                () -> assertEquals(1,          dto.getAplicaVigencia()),
                () -> assertEquals(FECHA_INICIO, dto.getFechaInicio()),
                () -> assertEquals(FECHA_FIN,    dto.getFechaFin())
        );
    }

    @Test
    @DisplayName("HomologaPolizaResponseDTO - campos opcionales pueden ser nulos")
    void responseDTO_nullOptionalFields() {
        HomologaPolizaResponseDTO dto = HomologaPolizaResponseDTO.builder()
                .id(1)
                .producto(749)
                .build();

        assertNull(dto.getFechaInicio());
        assertNull(dto.getFechaFin());
        assertNull(dto.getAplicaVigencia());
    }
}





