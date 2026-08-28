SELECT COUNT(*) FROM dbo.archivoAsientoAvalXml;
SELECT COUNT(*) FROM dbo.archivoAsientoCardifXml;



SELECT COUNT(*) FROM dbo.tmp_repavalcierre;
SELECT COUNT(*) FROM dbo.historicomov_aval;


SELECT familia, tipoMovimiento, nombreArchivo, cantidadLineas 
FROM dbo.archivoAsientoAvalXml ORDER BY familia, tipoMovimiento;

SELECT COUNT(*) FROM controlcierreaval;

SELECT id, Tipomovimiento, Fechacontabilizacion 
FROM historicomovimientos WHERE archivocargue = 'PRUEBA_COL_AVAL';
