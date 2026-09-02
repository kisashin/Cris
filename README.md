SELECT DB_NAME() AS base, o.name, o.create_date, o.modify_date, o.type_desc
FROM sys.objects o
WHERE o.name IN ('sp_XMLAsientosPru','sp_AsientoSiniestrosAdicionales',
                 'sp_CargaSiniestros','sp_CargaSiniestrosAlfa','NEOS_BCP_exec')
ORDER BY o.name;



SELECT name, base_object_name FROM sys.synonyms;


SELECT o.name, o.type_desc
FROM sys.sql_modules m
JOIN sys.objects o ON o.object_id = m.object_id
WHERE m.definition LIKE '%sp_XMLAsientosPru%'
ORDER BY o.name;
