USE SiniestrosWp;

SELECT idusuario, idautorizador, COUNT(*) AS total,
       MIN(Fechaproceso) AS desde, MAX(Fechaproceso) AS hasta
FROM novedadhistoricoindividual
GROUP BY idusuario, idautorizador
ORDER BY total DESC;

SELECT estado, tiponovedad, COUNT(*) AS total
FROM novedadhistoricoindividual
GROUP BY estado, tiponovedad;

SELECT TOP 20 CIE, COUNT(*) AS total
FROM historicomovimientos
WHERE CIE IS NOT NULL AND LTRIM(RTRIM(CIE)) <> ''
GROUP BY CIE ORDER BY total DESC;





SELECT i.name, i.type_desc, i.is_unique, i.is_primary_key,
       c.name AS columna, ic.key_ordinal
FROM sys.indexes i
JOIN sys.index_columns ic ON ic.object_id=i.object_id AND ic.index_id=i.index_id
JOIN sys.columns c ON c.object_id=i.object_id AND c.column_id=ic.column_id
WHERE i.object_id IN (OBJECT_ID('historicomovimientos'), OBJECT_ID('novedadhistoricoindividual'))
ORDER BY i.object_id, i.index_id, ic.key_ordinal;
