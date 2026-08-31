# NFR — Cierre Contable Centroamérica: eliminación de `bcp`/STCP y descarga de XML en pantalla

## Contexto

La generación de asientos contables de Centroamérica escribía los archivos XML en disco mediante `xp_cmdshell` + `bcp`, sobre la ruta compartida `d:\Carguesocios\Salida\XML\`. Un proceso externo (STCP) recogía esos archivos y los enviaba a SunSystems.

Este esquema tenía tres problemas:

- Dependencia de `xp_cmdshell` y de permisos de escritura del motor sobre una ruta de red.
- Uso de una tabla temporal global (`##xmlSinCen`) leída desde una segunda conexión abierta por `bcp`, con riesgo de bloqueos.
- El analista no tenía visibilidad ni control sobre los archivos generados.

## Alcance entregado

Se elimina `bcp` y la intervención de STCP. Los procedimientos almacenados devuelven las líneas del asiento como conjunto de resultados; el backend arma los archivos XML, los persiste y los expone para descarga desde la pantalla.

### Cambios en base de datos

- `sp_Gen_Xml_Siniestros_ReasegCentro`: se retira `xp_cmdshell` y `bcp`. Devuelve las líneas del XML como result set. `##xmlSinCen` pasa a tabla temporal local. `Line` pasa de `varchar(1500)` a `nvarchar(max)`.
- `sp_contabiliza_cardifCentro`: acumula las dos pasadas (movimientos normales y reversas) y devuelve un único result set con `Periodo`, `Pasada`, `id`, `Mv`, `Secuencia`, `Line`. Se agrega `SET NOCOUNT ON`. La lógica de negocio y el `UPDATE fechacontabilizacion` se mantienen sin cambios.
- Nueva tabla `archivoAsientoCentro`, siguiendo la convención de `archivoAsientoAval`, `archivoAsientoCardif` y `archivoAsientoEcosistemas`.

### Cambios en backend

- Componente `StoredProcedureExecutor`: ejecución de procedimientos almacenados con timeout configurable y cierre garantizado de statements y cursores. Reutilizable por los demás módulos de cierre.
- Persistencia de los XML generados en `archivoAsientoCentro`.
- Endpoints nuevos: consulta de archivos generados y descarga individual por identificador.
- Borrado de los archivos de la corrida anterior al iniciar una nueva generación.
- Operación transaccional: borrado, generación, armado, persistencia y marcación de contabilizados ocurren en una única transacción.

### Cambios en frontend

- Tabla con los archivos generados (fecha de proceso, periodo, tipo de movimiento, líneas, estado) y enlace de descarga por archivo.
- La tabla se carga al abrir la pantalla, de modo que los archivos siguen disponibles tras refrescar o cerrar el navegador.
- Diálogo de confirmación previo a la generación, advirtiendo que se eliminarán los registros anteriores.
- Componente de confirmación genérico, reutilizable por los demás módulos de cierre.

## Beneficios

- Se elimina la dependencia de `xp_cmdshell` y de permisos de escritura sobre rutas de red.
- Se elimina la tabla temporal global y la segunda conexión, junto con su riesgo de bloqueo.
- Los XML dejan de perderse al refrescar la pantalla.
- Si la generación falla, no quedan movimientos marcados como contabilizados sin su archivo correspondiente.
- El ejecutor de procedimientos y el diálogo de confirmación quedan disponibles para Perú, Colombia y Reaseguro.

## Fuera de alcance

Se identificaron dos comportamientos preexistentes del proceso legacy que se reproducen sin cambios en esta entrega y se reportan por separado:

- Los movimientos de tipo `Aumento Reserva` no llegan al XML pero sí quedan marcados como contabilizados.
- El archivo de `Objecion` se genera vacío; las objeciones viajan etiquetadas como `Liberacion`.

## Evidencia de pruebas

Ejecución con 98 movimientos pendientes:

| Archivo | Líneas |
|---|---|
| Constitucion | 204 |
| Liberacion | 28 |
| Pago | 216 |
| RevPago | 24 |

- Los archivos se conservan al refrescar la pantalla y se descargan correctamente.
- Los XML abren sin errores de formato y cierran en `</SSC>`.
- Con cero movimientos pendientes, la generación se rechaza y los archivos de la corrida anterior permanecen intactos.
- Forzando un fallo en la persistencia, los movimientos permanecen sin contabilizar.
- La estructura de cuentas coincide con la del archivo de producción.
