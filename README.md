EXEC sp_help 'dbo.archivoAsientoAval';

SELECT o.name AS objeto, o.type_desc
FROM sys.sql_modules m
INNER JOIN sys.objects o ON o.object_id = m.object_id
WHERE m.definition LIKE '%archivoAsientoAval%'
ORDER BY o.type_desc, o.name;


SELECT DB_NAME(), s.name, t.name
FROM sys.tables t INNER JOIN sys.schemas s ON s.schema_id = t.schema_id
WHERE t.name LIKE '%ArchivoAsiento%';
