USE [SiniestrosWp];
GO

-- Ver los nombres exactos
SELECT archivocargue, COUNT(*) 
FROM historicomovimientos 
WHERE Fechacontabilizacion IS NULL 
GROUP BY archivocargue;


-- Borrar los movimientos (ajusta los nombres)
DELETE FROM historicomovimientos 
WHERE archivocargue IN ('prueba.xlsx', 'prueba 2.xlsx');

-- Borrar las aperturas que insertaste a mano y quedaron huerfanas
DELETE hi
FROM historico_inicial hi
LEFT JOIN historicomovimientos hm ON hm.Llavesiniestro = hi.Llavesiniestro
WHERE hm.Llavesiniestro IS NULL
  AND hi.NumeroSiniestro LIKE '%2026A%';

-- Limpiar tablas de resultado
DELETE FROM archivoAsientoAvalXml;
DELETE FROM archivoAsientoCardifXml;
DELETE FROM archivoReporteAvalExcel;
DELETE FROM controlcierreaval;
DELETE FROM tmp_repavalcierre;
DELETE FROM historicomov_aval;
DELETE FROM tmpsiniestros;
GO


SELECT COUNT(*) FROM historicomovimientos WHERE Fechacontabilizacion IS NULL;
