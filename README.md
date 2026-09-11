-- ¿Que objetos escriben en historico_inicial?
SELECT OBJECT_SCHEMA_NAME(o.object_id) AS esquema,
       OBJECT_NAME(o.object_id) AS objeto,
       o.type_desc
FROM sys.sql_modules m
JOIN sys.objects o ON o.object_id = m.object_id
WHERE m.definition LIKE '%historico_inicial%'
  AND m.definition LIKE '%insert%';

-- ¿Hay triggers sobre historicomovimientos?
SELECT name, is_disabled 
FROM sys.triggers 
WHERE parent_id = OBJECT_ID('dbo.historicomovimientos');


SELECT OBJECT_NAME(object_id) AS objeto
FROM sys.sql_modules
WHERE definition LIKE '%historico_inicial%'
  AND (definition LIKE '%insert into historico_inicial%'
       OR definition LIKE '%INSERT INTO historico_inicial%');
