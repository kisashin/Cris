-- El generador (la pieza que falta)
EXEC sp_helptext 'sp_Gen_Xml_Siniestros_ReasegCentro';

-- Su equivalente Perú y el SP de contabilización Perú
EXEC sp_helptext 'sp_contabiliza_cardif_ext';

-- ¿Quién más toca el buffer? Confirma o descarta la contaminación cross-país
SELECT OBJECT_NAME(object_id), definition
FROM sys.sql_modules
WHERE definition LIKE '%TBL_Asientos_siniestro%';

-- ¿Hay escritura a disco?
SELECT OBJECT_NAME(object_id)
FROM sys.sql_modules
WHERE definition LIKE '%xp_cmdshell%' OR definition LIKE '%bcp %'
   OR definition LIKE '%OPENROWSET%';
