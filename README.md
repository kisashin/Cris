USE CardifWP;
EXEC sp_helptext 'dbo.sp_XMLAsientosPru';
EXEC sp_helptext 'dbo.sp_CargaSiniestrosAlfa';


USE CardifWP;
SELECT s.name AS esquema, o.name, o.type_desc, o.create_date, o.modify_date,
       CASE WHEN m.definition IS NULL THEN 'CIFRADO O SIN PERMISO' ELSE 'OK' END AS estado
FROM sys.objects o
JOIN sys.schemas s ON s.schema_id = o.schema_id
LEFT JOIN sys.sql_modules m ON m.object_id = o.object_id
WHERE o.name IN ('sp_XMLAsientosPru','sp_CargaSiniestrosAlfa','sp_AsientoSiniestrosAdicionales');



USE CardifWP;
SELECT p.name AS parametro, TYPE_NAME(p.user_type_id) AS tipo, p.max_length,
       p.has_default_value, p.default_value
FROM sys.parameters p
WHERE p.object_id = OBJECT_ID('dbo.sp_XMLAsientosPru')
ORDER BY p.parameter_id;



USE CardifWP;
SELECT OBJECT_NAME(object_id) AS objeto_que_llama
FROM sys.sql_modules
WHERE (definition LIKE '%sp_XMLAsientosPru%' OR definition LIKE '%sp_CargaSiniestrosAlfa%')
  AND OBJECT_NAME(object_id) NOT IN ('sp_XMLAsientosPru','sp_CargaSiniestrosAlfa');
  
SELECT name, definition FROM sys.sql_modules m
JOIN sys.objects o ON o.object_id = m.object_id
WHERE m.definition LIKE '%NEOS_BCP_exec%';


USE CardifWP;
SELECT producto, patron, layout FROM PatronxProd_siniestros
WHERE producto IN ('2011','2012','2014','2020','2028') ORDER BY producto;

SELECT * FROM Socios_Prod_Siniestros
WHERE producto IN ('2011','2012','2014','2020','2028') ORDER BY producto;

SELECT producto, ramo, cobertura, peso, valor, afectadox
FROM Cobertura_Prod_Xpln_Plz_Cnl
WHERE producto IN ('2011','2012','2014','2020','2028') ORDER BY producto, ramo;
