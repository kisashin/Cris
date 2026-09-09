USE SiniestrosWp;
SELECT s.name AS esquema, o.name, o.type_desc, o.create_date, o.modify_date,
       CASE WHEN m.definition IS NULL THEN 'SIN DEFINICION (cifrado o sin permiso)' ELSE 'OK' END AS estado
FROM sys.objects o
JOIN sys.schemas s ON s.schema_id = o.schema_id
LEFT JOIN sys.sql_modules m ON m.object_id = o.object_id
WHERE o.name LIKE 'sp_Gen_Xml_Siniestros%' OR o.name LIKE 'sp_contabiliza%';

SELECT OBJECT_ID('SiniestrosWp.dbo.sp_Gen_Xml_Siniestros_ReasegCardif');
SELECT HAS_PERMS_BY_NAME('SiniestrosWp.dbo.sp_Gen_Xml_Siniestros_ReasegCardif','OBJECT','VIEW DEFINITION');
