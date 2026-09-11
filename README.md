USE [SiniestrosWp];
GO

DELETE FROM historicomovimientos WHERE archivocargue LIKE 'prueba%';
DELETE FROM archivoAsientoAvalXml;
DELETE FROM archivoAsientoCardifXml;
DELETE FROM archivoReporteAvalExcel;
DELETE FROM controlcierreaval;
DELETE FROM tmp_repavalcierre;
DELETE FROM historicomov_aval;
DELETE FROM tmpsiniestros;
DELETE FROM HistoricoasientosPru;
GO

-- Debe dar 0
SELECT COUNT(*) FROM historicomovimientos WHERE Fechacontabilizacion IS NULL;
SELECT COUNT(*) FROM controlcierreaval;


SELECT hi.Aval, COUNT(*)
FROM historicomovimientos hm
LEFT JOIN historico_inicial hi ON hi.Llavesiniestro = hm.Llavesiniestro
WHERE hm.Fechacontabilizacion IS NULL
GROUP BY hi.Aval;
