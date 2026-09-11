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
