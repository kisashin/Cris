Comparativo: comportamiento de la grilla de reporte en Cierre Mensual de Aval
Cómo funciona en el sistema actual (legado)

La pantalla muestra la sección "Reporte de movimientos" con el enlace de consulta. Debajo aparece una grilla que solo se despliega cuando hay información disponible; cuando no la hay, el sistema muestra el mensaje "No registros para consultar" en lugar de la grilla.

La captura adjunta, tomada del ambiente de pruebas del sistema actual, muestra exactamente ese caso: sin registros pendientes, la grilla no se despliega y solo se ve el mensaje.

Cómo funciona en la solución migrada

El comportamiento es el mismo. La grilla se muestra únicamente cuando existen movimientos por reportar, y en caso contrario aparece el mismo mensaje "No registros para consultar".

La diferencia está en cómo se obtiene el archivo, no en cuándo se muestra la grilla:

	Sistema actual	Solución migrada
Acción del usuario	Botón "Generar"	Enlace "Descargar Excel"
Qué ocurre	Marca el registro como pendiente y un proceso automatizado genera el archivo en un servidor de archivos	El archivo se genera y se descarga en el momento
Tiempo de espera	El usuario debe esperar a que el proceso automatizado se ejecute	Inmediato
Dependencias	Requiere el proceso automatizado activo	Ninguna
Consideración sobre la disponibilidad del archivo

En ambos casos el reporte refleja los movimientos pendientes por contabilizar al momento de la consulta. Una vez ejecutada la generación de asientos contables, esos movimientos quedan contabilizados y el reporte deja de mostrarlos, tal como ocurre hoy.

La diferencia práctica es que en el sistema actual el archivo permanecía en el servidor hasta la siguiente ejecución, mientras que en la solución migrada se genera bajo demanda. Si el área requiere conservar el reporte de cierres ya procesados para consulta posterior, esa funcionalidad no existe en ninguna de las dos versiones y debería evaluarse por separado.
