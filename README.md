USE SiniestrosWp;
SELECT t.name AS tabla, c.column_id, c.name AS columna,
       ty.name AS tipo, c.max_length, c.is_nullable
FROM sys.columns c
JOIN sys.tables t  ON t.object_id = c.object_id
JOIN sys.types ty  ON ty.user_type_id = c.user_type_id
WHERE t.name IN ('historicomovimientos','novedadhistoricoindividual')
ORDER BY t.name, c.column_id;
