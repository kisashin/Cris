SELECT i.name AS indice, c.name AS columna
FROM sys.index_columns ic
JOIN sys.indexes i ON i.object_id = ic.object_id AND i.index_id = ic.index_id
JOIN sys.columns c ON c.object_id = ic.object_id AND c.column_id = ic.column_id
WHERE ic.object_id = OBJECT_ID('dbo.tmpsiniestros_ext') AND c.name LIKE 'Cobertura%';
