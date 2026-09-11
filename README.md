USE [SiniestrosWp];
GO

DELETE FROM historicomovimientos WHERE archivocargue LIKE 'prueba%';

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


SELECT COUNT(*) 
FROM historicomovimientos hm
LEFT JOIN historico_inicial hi ON hi.Llavesiniestro = hm.Llavesiniestro
WHERE hm.Fechacontabilizacion IS NULL AND hi.Llavesiniestro IS NULL;
