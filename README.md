SELECT familia, tipoMovimiento, nombreArchivo, cantidadLineas 
FROM dbo.archivoAsientoCardifXml 
ORDER BY familia, tipoMovimiento;

SELECT id, Tipomovimiento, tipocoaseguro, Fechacontabilizacion 
FROM historicomovimientos 
WHERE archivocargue IN ('PRUEBA_COL_CARDIF', 'PRUEBA_COL_COASEG')
ORDER BY id;
