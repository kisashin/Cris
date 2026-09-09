Cierre Mensual de Directas (Cardif) — Generación de XML por pantalla
Contexto

Igual que en Aval: el botón marcaba archivoAsientoCardif como pendiente y un paquete SSIS ejecutaba el proceso contable, que a su vez encadenaba los procedimientos de coaseguro y de directas, dejando los XML en un file server.

Alcance entregado
Cambios en base de datos
sp_XMLAsientosPru: mismo cambio descrito en el módulo de Aval; el procedimiento es compartido por ambos cierres.
sp_Gen_Xml_Siniestros_ReasegCardif y sp_Gen_Xml_Siniestros_CoaseguroC: se retira el bloque de bcp y la copia al file server. Devuelven las líneas como conjunto de resultados, las tablas temporales globales pasan a locales y la columna Line pasa a nvarchar(max). El procedimiento de coaseguro distingue en su salida las dos familias que produce.
sp_contabiliza_cardif y sp_contabiliza_coaseguro: acumulan la salida de los generadores y devuelven un único conjunto de resultados con la misma estructura de columnas, de modo que ambos se leen con el mismo mapeo.
Nueva tabla archivoAsientoCardifXml, con la misma estructura que la de Aval.
Cambios en backend
Endpoints nuevos: generación de asientos, consulta de archivos generados y descarga individual por identificador.
La generación ejecuta los procedimientos de coaseguro y de directas en ese orden, dentro de una misma transacción, replicando la secuencia del paquete SSIS.
Validación explícita de que el cierre de Aval haya sido ejecutado previamente. En el proceso anterior esa dependencia estaba implícita en una condición del paquete: si no se cumplía, el proceso no hacía nada y no dejaba constancia. Ahora se devuelve un mensaje de error al usuario.
Borrado de los archivos de la corrida anterior, persistencia de los generados y operación transaccional, igual que en Aval.
Cambios en frontend
Botón de generación con diálogo de confirmación y tabla de archivos descargables, con las mismas columnas que Aval.
El enlace al servidor de reportes se conserva sin cambios.
Pruebas

Ejecución de extremo a extremo con el archivo de cargue del periodo. Se procesaron 344 movimientos y se generaron ocho archivos correspondientes a las cuatro familias del módulo, con resultados reproducibles entre corridas. Se validó además el rechazo del proceso cuando el cierre de Aval no ha sido ejecutado. Cobertura unitaria por encima del 90% en backend y frontend.
