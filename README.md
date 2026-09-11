SELECT COUNT(*) FROM historicomovimientos 
WHERE Fechacontabilizacion IS NOT NULL AND archivocargue LIKE 'prueba%';

SELECT COUNT(*) FROM controlcierreaval;

SELECT familia, tipoMovimiento, nombreArchivo, cantidadLineas 
FROM archivoAsientoAvalXml;
