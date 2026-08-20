-- 1. ¿Hay unique/PK sobre IDCARVAJAL? Define si puedo generar valores libremente
SELECT i.name, i.is_unique, i.is_primary_key, c.name AS columna
FROM sys.indexes i
JOIN sys.index_columns ic ON ic.object_id = i.object_id AND ic.index_id = i.index_id
JOIN sys.columns c ON c.object_id = ic.object_id AND c.column_id = ic.column_id
WHERE i.object_id = OBJECT_ID('dbo.historicomovimientos_ext');

-- 2. Rango actual, para elegir valores que no choquen
SELECT MAX(IDCARVAJAL) AS max_idcarvajal FROM dbo.historicomovimientos_ext WITH (NOLOCK);
