USE [SiniestrosWp];
GO

-- Borrar los movimientos de prueba (ajusta los nombres)
DELETE FROM historicomovimientos WHERE archivocargue LIKE 'prueba%';

-- Borrar las aperturas que insertamos a mano
DELETE hi
FROM historico_inicial hi
LEFT JOIN historicomovimientos hm ON hm.Llavesiniestro = hi.Llavesiniestro
WHERE hm.Llavesiniestro IS NULL
  AND hi.NumeroSiniestro LIKE '%2026A%';

DELETE FROM archivoAsientoAvalXml;
DELETE FROM archivoAsientoCardifXml;
DELETE FROM archivoReporteAvalExcel;
DELETE FROM controlcierreaval;
DELETE FROM tmp_repavalcierre;
DELETE FROM historicomov_aval;
DELETE FROM tmpsiniestros;
GO

SELECT hi.Aval, COUNT(*)
FROM historicomovimientos hm
JOIN historico_inicial hi ON hi.Llavesiniestro = hm.Llavesiniestro
WHERE hm.Fechacontabilizacion IS NULL
GROUP BY hi.Aval;
