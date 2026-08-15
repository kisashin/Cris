SELECT o.name, o.type_desc, m.definition
FROM sys.sql_modules m
JOIN sys.objects o ON o.object_id = m.object_id
WHERE m.definition LIKE '%archivoAsientoAval%'
   OR m.definition LIKE '%tmp_repavalcierre%';
