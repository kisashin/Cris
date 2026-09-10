USE [SiniestrosWp];
GO

-- Verificar antes de borrar
SELECT COUNT(*) FROM historicomovimientos 
WHERE archivocargue IN ('Cargue Col Pruebas URL Sep.xlsx', 'Cargue Col 11 08 2026.xlsx');

-- Borrar los dos cargues viejos
DELETE FROM historicomovimientos 
WHERE archivocargue IN ('Cargue Col Pruebas URL Sep.xlsx', 'Cargue Col 11 08 2026.xlsx');

-- Limpiar resultados y tablas de trabajo
DELETE FROM archivoAsientoAvalXml;
DELETE FROM archivoAsientoCardifXml;
DELETE FROM archivoReporteAvalExcel;
DELETE FROM controlcierreaval;
DELETE FROM tmp_repavalcierre;
DELETE FROM historicomov_aval;
DELETE FROM tmpsiniestros;
GO


SELECT COUNT(*) FROM historicomovimientos WHERE Fechacontabilizacion IS NULL;


SELECT hi.Aval, COUNT(*) 
FROM historicomovimientos hm
JOIN historico_inicial hi ON hi.Llavesiniestro = hm.Llavesiniestro
WHERE hm.Fechacontabilizacion IS NULL
GROUP BY hi.Aval;
