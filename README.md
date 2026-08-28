USE [SiniestrosWp];
GO

-- 1. Borrar los movimientos de prueba
DELETE FROM historicomovimientos 
WHERE archivocargue IN (
    'PRUEBA_COL_AVAL', 'PRUEBA_COL_CARDIF', 'PRUEBA_COL_COASEG');

DELETE FROM historico_inicial 
WHERE Llavesiniestro IN (
    'TEST-AVAL-001', 'TEST-CARDIF-001', 'TEST-COASEG-001');

-- 2. Vaciar los archivos generados
DELETE FROM archivoAsientoAvalXml;
DELETE FROM archivoAsientoCardifXml;

-- 3. Vaciar el control de orden
DELETE FROM controlcierreaval;

-- 4. Vaciar las tablas del reporte
DELETE FROM tmp_repavalcierre;
DELETE FROM historicomov_aval;

-- 5. Vaciar los buffers de trabajo de los SP
DELETE FROM tmpsiniestros;
DELETE FROM Hist_Siniestro_Hogar;
DELETE FROM HistoricoasientosPru;
GO



SELECT 'historicomovimientos prueba' t, COUNT(*) c 
FROM historicomovimientos 
WHERE archivocargue LIKE 'PRUEBA_COL%'
UNION ALL SELECT 'archivoAsientoAvalXml', COUNT(*) FROM archivoAsientoAvalXml
UNION ALL SELECT 'archivoAsientoCardifXml', COUNT(*) FROM archivoAsientoCardifXml
UNION ALL SELECT 'controlcierreaval', COUNT(*) FROM controlcierreaval
UNION ALL SELECT 'tmp_repavalcierre', COUNT(*) FROM tmp_repavalcierre
UNION ALL SELECT 'historicomov_aval', COUNT(*) FROM historicomov_aval
UNION ALL SELECT 'tmpsiniestros', COUNT(*) FROM tmpsiniestros;


SELECT COUNT(*), MIN(wProc), MAX(wProc) FROM Hist_Siniestro_Hogar;

SELECT COUNT(*) FROM historicomovimientos WHERE Fechacontabilizacion IS NULL;
