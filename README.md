SELECT archivocargue, COUNT(*) AS total,
       SUM(CASE WHEN Fechacontabilizacion IS NULL THEN 1 ELSE 0 END) AS pendientes,
       MIN(fechacargue) AS primera, MAX(fechacargue) AS ultima
FROM historicomovimientos
GROUP BY archivocargue
ORDER BY MAX(fechacargue) DESC;


SELECT archivocargue, COUNT(*), MIN(fechacargue), MAX(fechacargue)
FROM historicomovimientos
GROUP BY archivocargue
ORDER BY MAX(fechacargue) DESC;


USE [SiniestrosWp];
GO

-- 1. Ver que se va a borrar (correr primero, sin borrar nada)
SELECT COUNT(*) FROM historicomovimientos 
WHERE archivocargue = 'NOMBRE_DEL_ARCHIVO';

-- 2. Borrar los movimientos
DELETE FROM historicomovimientos 
WHERE archivocargue = 'NOMBRE_DEL_ARCHIVO';

-- 3. Borrar las aperturas que quedaron huerfanas
DELETE hi
FROM historico_inicial hi
LEFT JOIN historicomovimientos hm ON hm.Llavesiniestro = hi.Llavesiniestro
WHERE hm.Llavesiniestro IS NULL;

-- 4. Limpiar tablas de trabajo y resultados
DELETE FROM archivoAsientoAvalXml;
DELETE FROM archivoAsientoCardifXml;
DELETE FROM archivoReporteAvalExcel;
DELETE FROM controlcierreaval;
DELETE FROM tmp_repavalcierre;
DELETE FROM historicomov_aval;
DELETE FROM tmpsiniestros;
GO
