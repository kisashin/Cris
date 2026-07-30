USE CardifWP;
SELECT OBJECT_DEFINITION(OBJECT_ID('dbo.sp_CargaSiniestros'))     AS carga;
SELECT OBJECT_DEFINITION(OBJECT_ID('dbo.sp_CargaSiniestrosAlfa')) AS alfa;


-- qué recibe
SELECT p.name, TYPE_NAME(p.user_type_id) tipo, p.max_length, p.is_output
FROM sys.parameters p
WHERE p.object_id IN (OBJECT_ID('dbo.sp_CargaSiniestros'),
                      OBJECT_ID('dbo.sp_CargaSiniestrosAlfa'))
ORDER BY p.object_id, p.parameter_id;

-- qué tablas toca
SELECT referenced_entity_name, referenced_minor_name, is_selected, is_updated
FROM sys.dm_sql_referenced_entities('dbo.sp_CargaSiniestros','OBJECT');

-- quién lo llama desde la misma base
SELECT o.name, o.type_desc
FROM sys.sql_modules m JOIN sys.objects o ON o.object_id = m.object_id
WHERE m.definition LIKE '%sp_CargaSiniestros%';


SELECT o.name FROM sys.sql_modules m
JOIN sys.objects o ON o.object_id = m.object_id
WHERE m.definition LIKE '%RVARC%';
