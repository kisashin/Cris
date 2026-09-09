Cierre Mensual de Aval — Generación de XML por pantalla
Contexto

El botón de generación de asientos marcaba el registro de archivoAsientoAval como pendiente y un paquete SSIS, mediante polling sobre ese estado, ejecutaba el proceso contable y dejaba los archivos XML en un file server. El reporte mensual de movimientos seguía el mismo esquema con la tabla tmp_repavalcierre. Al retirarse esas reglas del SSIS, ambos procesos deben ejecutarse desde la pantalla.

Alcance entregado

Se elimina la dependencia de los paquetes SSIS y de bcp/xp_cmdshell. Los procedimientos devuelven las líneas del asiento como conjunto de resultados, el backend arma los archivos XML, los persiste y los expone para descarga.

Cambios en base de datos
sp_XMLAsientosPru: se habilita el parámetro @XmlDestino, que ya existía en la firma sin uso. Con valor PANTALLA devuelve el XML como conjunto de resultados y omite la escritura a disco; con el valor por defecto conserva el comportamiento actual, de modo que los demás consumidores no se ven afectados.
sp_Gen_Xml_Siniestros_ReasegAlfa: se retira el bloque de bcp y la copia al file server. Devuelve las líneas como conjunto de resultados, la tabla temporal global pasa a local y la columna Line pasa a nvarchar(max).
sp_contabiliza_aval: acumula la salida de los generadores de las dos pasadas y devuelve un único conjunto de resultados con familia, periodo, pasada, tipo de movimiento, secuencia y línea. La lógica de negocio y la marcación de contabilizados se mantienen sin cambios.
Nueva tabla archivoAsientoAvalXml, siguiendo la convención de archivoAsientoCentro con una columna adicional de familia.
Cambios en backend
Endpoints nuevos: generación de asientos, consulta de archivos generados y descarga individual por identificador.
Endpoint de descarga del reporte mensual en formato Excel. Ejecuta el procedimiento de generación y arma el archivo con el mismo layout y nombre que producía el paquete SSIS, sin pasar por tabla de estado.
Consulta del estado del reporte basada en los movimientos pendientes por contabilizar, en reemplazo de la lectura de tmp_repavalcierre, cuyo contenido residual producía falsos positivos.
Borrado de los archivos de la corrida anterior al iniciar una nueva generación.
Operación transaccional: borrado, ejecución, armado, persistencia y marcación de contabilizados ocurren en una única transacción.
Reutilización del ejecutor de procedimientos almacenados existente, al que se agrega una variante que selecciona el conjunto de resultados correspondiente cuando el procedimiento devuelve varios.
Cambios en frontend
Botón de generación con diálogo de confirmación previo, advirtiendo que se eliminarán los registros anteriores.
Tabla con los archivos generados (fecha de proceso, periodo, origen, tipo de movimiento, líneas, estado) y enlace de descarga por archivo. Se carga al abrir la pantalla, de modo que los archivos siguen disponibles tras refrescar o cerrar el navegador.
La sección del reporte mensual se muestra únicamente cuando existen movimientos pendientes y ofrece descarga directa del Excel.
El enlace al servidor de reportes se conserva sin cambios.
Pruebas

Ejecución de extremo a extremo con el archivo de cargue del periodo. Se procesaron 93 movimientos y se generaron los archivos de las familias correspondientes, con resultados reproducibles entre corridas. Cobertura unitaria por encima del 90% en backend y frontend.
