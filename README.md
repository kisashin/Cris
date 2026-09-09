Migración Reaseguro — Asientos Siniestros
Objetivo

Eliminar la dependencia de bcp / xp_cmdshell / file server en el módulo Reaseguro, dejando la carga de archivos y la descarga de XML directamente en pantalla, siguiendo el patrón ya implementado en Centroamérica y Colombia.

Contexto del bloqueante

El módulo estaba aprobado funcionalmente pero no podía pasar a TEST: el SP copiaba el XML a \\amcobgfp01wp\Soluciones\T_CONTABILIDAD\XML_RESERVA mediante xp_cmdshell, y en TEST no existe visibilidad de la base de datos hacia el file server. Esos permisos no van a otorgarse.

La migración elimina el requisito en lugar de solicitarlo.

Cambios en base de datos — CardifWP

sp_XMLAsientosPru
Se activó el parámetro @XmlDestino (ya existente en la firma, default 'SUN'). Con valor 'PANTALLA' el procedimiento omite la escritura por bcp, la copia a XML_RESERVA y el net use, y devuelve un único result set con Tipo_Diario, NombreArchivo y Contenido. Los demás consumidores no pasan el parámetro y conservan el comportamiento anterior. La tabla temporal ##sp_HistoricoAsientosPru pasó a local (#).

sp_CargaSiniestrosAlfa
Se eliminaron el descubrimiento de archivos por dir, el cursor, el bulk insert y el move a Procesados\. Se agregó el parámetro @Archivo. El procedimiento conserva la limpieza de datos y la inserción a CargaSiniestrosAlfa con DBO.FFLOAT().

archivoAsientoReaseguro (nueva)
Persiste los XML generados para su descarga. Clave única por producto, tipo de diario y periodo contable.

Cambios en backend — ws-cierres
POST /v1/claim-accounting/load pasó a multipart/form-data: recibe archivo, producto y usuario. Valida extensión y que el nombre corresponda al patrón del producto en PatronxProd_siniestros. Parsea el CSV, inserta por lotes en tmpCargaSiniestrosAlfa y ejecuta el procedimiento de carga.
POST /v1/claim-accounting/send pasó a transaccional. Genera los tres tipos de diario, reemplaza los archivos previos del producto y persiste los nuevos. Si falla, no se borra ni se marca nada.
GET /v1/claim-accounting/files — lista los archivos del periodo contable actual.
GET /v1/claim-accounting/files/{id}/download — descarga por bytes con Content-Disposition.
Se eliminó el ReentrantLock, innecesario tras el paso a tabla temporal local.
Errores de validación mapeados a 400 y 404 con mensaje legible.

Cobertura: 100% en repositorio, servicio y controller; 97% en el helper de lectura de archivos.

Cambios en frontend — closingcardiffront
Botón Cargar convertido en selector de archivo más acción de carga.
Grilla de archivos generados con descarga por fila.
Diálogo de confirmación antes de generar, indicando que los archivos previos del producto se reemplazan.
Botón "Enviar" renombrado a "Generar XML".
Corrección de la ruta del ítem Asientos Siniestros.
Ocultado el botón Genera XML en Cierre Cardif Perú a solicitud del negocio.
Retirados del menú los ítems sin implementación: Cardif, Reportes Historizados y Reaseguro Cuenta Técnica.
Validación realizada

Se ejecutó el flujo completo en DEV con archivo real del proveedor (producto 2020, 232 registros): carga, generación de asiento, registro, total por cuenta, generación de los tres XML y descarga. Se verificó codificación de caracteres, conversión de montos, reemplazo de archivos al regenerar y no afectación de otros productos. Se confirmó que no se escriben archivos en disco.
