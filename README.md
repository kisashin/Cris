Documentación — Módulo Homologación Póliza Alfa
Proyecto
ws-closing-claims — Migración ASP.NET WebForms → Spring Boot 2.6.6 (Java 1.8) + Angular
Tabla
dbo.homologaprod_alfa (SQL Server)
Estado
PR aprobado por líder técnico → desplegado en DEV → promovido a TEST
1. Descripción funcional
CRUD de homologaciones de pólizas Alfa, equivalente a la página legacy de mantenimiento:
Legacy
Migrado
CargarGridView1
GET /v1/homologacion-poliza-alfa?producto={code}
BtnGuardar_Click (id = 0)
POST /v1/homologacion-poliza-alfa
BtnGuardar_Click (id ≠ 0)
PUT /v1/homologacion-poliza-alfa/{id}
btnEliminar_Click
DELETE /v1/homologacion-poliza-alfa/{id}
2. Backend
Paquete base: co.com.bnpparibas.cardif.closingclaims
Componente
Clase
Controller
api.HomologationPolicyAlfaController
DTOs
domain.dtos.homologation.HomologationPolicyRequestDTO /
HomologationPolicyResponseDTO (@Builder)
Entidad
domain.entity.HomologationPolicyAlfa
Servicio
domain.services.IHomologationPolicyAlfaService /
impl.HomologationPolicyAlfaServiceImpl
Mapper
domain.util.helpers.HomologationPolicyAlfaMapper (MapStruct)
Repositorio
infraestructure.repository.HomologationPolicyAlfaRepository
(findByProducto, query nativa)
Endpoints
Headers comunes opcionales: _p, correlation_id, request_id. Respuesta con envelope
ResponseModel (correlationId, header.returnCode, bodyResponse).
