# Documentación — Módulo Homologación Póliza Alfa

| | |
|---|---|
| **Proyecto** | `ws-closing-claims` — Migración ASP.NET WebForms → Spring Boot 2.6.6 (Java 1.8) + Angular |
| **Tabla** | `dbo.homologaprod_alfa` (SQL Server) |
| **Estado** | PR aprobado por líder técnico → desplegado en DEV → promovido a TEST |

---

## 1. Descripción funcional

CRUD de homologaciones de pólizas Alfa, equivalente a la página legacy de mantenimiento:

| Legacy | Migrado |
|---|---|
| `CargarGridView1` | `GET /v1/homologacion-poliza-alfa?producto={code}` |
| `BtnGuardar_Click` (id = 0) | `POST /v1/homologacion-poliza-alfa` |
| `BtnGuardar_Click` (id ≠ 0) | `PUT /v1/homologacion-poliza-alfa/{id}` |
| `btnEliminar_Click` | `DELETE /v1/homologacion-poliza-alfa/{id}` |

---

## 2. Backend

**Paquete base:** `co.com.bnpparibas.cardif.closingclaims`

| Componente | Clase |
|---|---|
| Controller | `api.HomologationPolicyAlfaController` |
| DTOs | `domain.dtos.homologation.HomologationPolicyRequestDTO` / `HomologationPolicyResponseDTO` (`@Builder`) |
| Entidad | `domain.entity.HomologationPolicyAlfa` |
| Servicio | `domain.services.IHomologationPolicyAlfaService` / `impl.HomologationPolicyAlfaServiceImpl` |
| Mapper | `domain.util.helpers.HomologationPolicyAlfaMapper` (MapStruct) |
| Repositorio | `infraestructure.repository.HomologationPolicyAlfaRepository` (`findByProducto`, query nativa) |

### Endpoints

Headers comunes opcionales: `_p`, `correlation_id`, `request_id`. Respuesta con envelope `ResponseModel` (`correlationId`, `header.returnCode`, `bodyResponse`).

| Método | Ruta | Éxito | Body |
|---|---|---|---|
| GET | `/v1/homologacion-poliza-alfa?producto={int}` | 200 | Lista (vacía si no hay coincidencias) |
| POST | `/v1/homologacion-poliza-alfa` | 201 | Registro creado con `id` |
| PUT | `/v1/homologacion-poliza-alfa/{id}` | 200 | Registro actualizado |
| DELETE | `/v1/homologacion-poliza-alfa/{id}` | 200 | `"Record deleted successfully"` |

### Request body (POST/PUT) y validaciones

```json
{
  "productCode": 749,
  "branchCode": 31,
  "policyNumber": "0000490",
  "appliesValidity": 0,
  "startDate": "2024-01-01",
  "endDate": "2024-12-31"
}
```

| Campo | Validación |
|---|---|
| `productCode`, `branchCode` | `@NotNull`, `@Positive` |
| `policyNumber` | `@NotBlank`, `@Size(max=200)` |
| `appliesValidity` | `@NotNull`, valores 0/1 |
| `startDate`, `endDate` | `@NotNull`, formato `yyyy-MM-dd` (`@JsonFormat`) |

### Capa de servicio

- **Transaccionalidad:** `@Transactional(readOnly = true)` en consulta; `@Transactional` en create/update/delete.
- **Regla de negocio:** `validateDateRange` exige `startDate ≤ endDate`; lanza `BusinessException` 400 **antes** de cualquier acceso a BD (en update, antes incluso del `findById`).
- **Existencia previa:** update usa `findById().orElseThrow` y delete usa `existsById`; `id` inexistente → `BusinessException` 404 con mensaje `"Record not found with id: {id}"`.
- **Errores de infraestructura:** toda excepción de repositorio/BD se registra vía SLF4J (incluyendo `correlationId` y `requestId` para trazabilidad) y se relanza como `BusinessException` 500. En update, las `BusinessException` se propagan sin re-envolver.

### Mapeo de datos

| Columna BD | Entidad | DTO | Tipo |
|---|---|---|---|
| `id` | `id` | `id` (response) | Integer (IDENTITY) |
| `producto` | `producto` | `productCode` | Integer |
| `ramo` | `ramo` | `branchCode` | Integer |
| `nro_poliza` | `nroPoliza` | `policyNumber` | String(200) |
| `aplicavigencia` | `aplicaVigencia` | `appliesValidity` | Integer (0/1) |
| `fechainicio` | `fechaInicio` | `startDate` | LocalDate |
| `fechafin` | `fechaFin` | `endDate` | LocalDate |

Notas técnicas: `@Column` en minúsculas (evita `SQLGrammarException` por naming strategy camelCase→snake_case), `Integer` para columnas `int`, traducción español↔inglés centralizada en el mapper MapStruct (incluye `updateEntity` con `@MappingTarget` que preserva el `id`).

---

## 3. Frontend

**Ruta:** `src/app/views/claims-closing/movements-col/homologation-policy-alfa/`

- **Componente** (`HomologationPolicyAlfaComponent`): búsqueda por producto (requerido), tabla con `app-report-table` (`IMetaColumn` con acciones editar/eliminar), formulario reactivo de alta/edición. `onSave()` decide POST o PUT según `editingId`, convierte radio Sí/No → 1/0 y normaliza fechas a `yyyy-MM-dd` con `formatDate()`.
- **Servicio** (`HomologationPolicyAlfaService`): patrón de `load-movements` — `INewGeneralResponse<T>`, base URL desde `environment.urlAPIClosingClaimsBackEnd`, headers `_p`/`correlation_id`/`request_id` con `crypto.randomUUID()`.
- **Validaciones:** `productCode`, `branchCode`, `policyNumber`, `appliesValidity` requeridos; validador cruzado `dateRangeValidator` (startDate ≤ endDate) con mensaje en pantalla.
- Tras crear/editar/eliminar se relanza `onSearch()` para refrescar la tabla.

---

## 4. Pruebas unitarias

| Capa | Clase | Tests |
|---|---|---|
| Controller | `HomologationPolicyAlfaControllerTest` | 8 — caminos felices, lista vacía, propagación de excepciones |
| Servicio | `HomologationPolicyAlfaServiceImplTest` | 13 — mapeo, 404, 400 por rango de fechas (sin tocar BD), 500 por fallas de repositorio |
| Entidad | `HomologationPolicyAlfaTest` | 3 |
| DTOs | `HomologationPolicyDTOsTest` | 7 — incluye Bean Validation real |
| Frontend | `homologation-policy-alfa.component.spec.ts` | 14 — formularios, CRUD, validador de fechas, manejo de error en búsqueda |

Objetivo: ≥ 90 % JaCoCo. Las clases `Builder` de Lombok reducen la métrica por clase (comportamiento conocido del proyecto). Ejecución vía IntelliJ por restricciones de red Maven/Nexus.
