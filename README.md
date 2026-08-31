NFR: Migración cierre contable Colombia (Aval y Cardif) — XML por pantalla

Contexto

Los cierres contables de Aval y Cardif (Directas) generaban sus archivos XML mediante bcp y xp_cmdshell, escribiendo a un file server. El disparo dependía de dos paquetes SSIS que hacían polling sobre el estado de las tablas archivoAsientoAval y archivoAsientoCardif. Esas reglas del SSIS se van a retirar, por lo que el proceso debe ejecutarse desde la pantalla y los archivos quedar disponibles para descarga, siguiendo el patrón ya implementado en Centroamérica.

Subtarea 1 — Ajuste de procedimientos almacenados

Eliminar bcp y xp_cmdshell de los generadores; devolver las líneas del asiento como conjunto de resultados.

sp_XMLAsientosPru: se activa el parámetro existente @XmlDestino; con valor PANTALLA devuelve el XML como result set, y conserva el comportamiento actual con el valor por defecto para no afectar a otros consumidores.
sp_Gen_Xml_Siniestros_ReasegAlfa, sp_Gen_Xml_Siniestros_ReasegCardif y sp_Gen_Xml_Siniestros_CoaseguroC: se retira el bloque bcp, las tablas temporales globales pasan a locales y la columna Line pasa a nvarchar(max).
sp_contabiliza_aval, sp_contabiliza_cardif y sp_contabiliza_coaseguro: acumulan la salida de los generadores y devuelven un único result set con familia, periodo, pasada, movimiento, secuencia y línea.

Sugerido: 8 h

Subtarea 2 — Modelo de datos

Creación de las tablas archivoAsientoAvalXml y archivoAsientoCardifXml para persistir los XML generados, siguiendo la convención de archivoAsientoCentro más una columna de familia. Las tablas actuales se mantienen sin cambios hasta que se retiren los paquetes SSIS.

Sugerido: 2 h

Subtarea 3 — Backend
Nuevos endpoints por módulo: generación de asientos, consulta de archivos generados y descarga individual.
Endpoint adicional en Aval para la descarga del reporte mensual de movimientos en Excel, reemplazando el archivo que producía el paquete SSIS.
Operación transaccional: borrado de la corrida anterior, ejecución, armado, persistencia y marcación de contabilizados en una única transacción.
Validación explícita del orden Aval → Cardif, que en el proceso anterior estaba implícita en el paquete SSIS y fallaba en silencio.
Reutilización del componente de ejecución de procedimientos ya existente.
Cobertura unitaria por encima del 90%.

Sugerido: 16 h

Subtarea 4 — Frontend
Pantallas de Cierre Aval y Cierre Cardif alineadas con Centroamérica: botón de generación con diálogo de confirmación y tabla de archivos descargables.
La tabla se carga al abrir la pantalla, de modo que los archivos siguen disponibles tras refrescar o cerrar el navegador.
En Aval, el reporte mensual pasa a descarga directa; la sección se muestra solo cuando existen movimientos pendientes.
Specs con cobertura por encima del 90%.

Sugerido: 10 h

Subtarea 5 — Pruebas y despliegue
Pruebas de extremo a extremo con el archivo de cargue del periodo.
Empaquetado de los procedimientos en Liquibase.
Validación de resultados con el área usuaria.

Sugerido: 8 h

Hallazgos para registrar aparte

Estos salieron durante el análisis y no forman parte del alcance. Conviene dejarlos como comentario en la tarea o como incidencias separadas:

sp_Genera_RepAval_cierre divergente entre ambientes. La versión de DEV tenía un SET IDENTITY_INSERT sobre una tabla sin columna identidad, lo que impedía su ejecución. Se alineó con la versión de producción.
Movimientos sin apertura registrada. En la prueba con datos reales, 650 de 1087 movimientos correspondían a siniestros sin registro en historico_inicial, por lo que quedaron fuera de ambos cierres. Se atribuye a que el ambiente de desarrollo no tiene el histórico completo, pero conviene confirmarlo.
sp_contabiliza_cardif limpia marcaavalpos en toda la tabla, sin acotar a los movimientos procesados. Comportamiento heredado.
Nombres de archivo con criterios distintos. Aval usa getdate()-5 y Cardif la fecha registrada en controlcierreaval, por lo que los archivos de una misma corrida pueden salir con fechas diferentes.
