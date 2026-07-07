-- Parado en SiniestrosWp. Confirma en el dropdown de base de SSMS.
SELECT OBJECT_DEFINITION(OBJECT_ID('dbo.sp_AsientosSiniestros')) AS cuerpo;

-- Parado en SiniestrosWp
SELECT 
    OBJECT_NAME(object_id) AS procedimiento,
    LEN(OBJECT_DEFINITION(object_id)) AS caracteres_de_logica
FROM sys.objects
WHERE name IN ('sp_AsientosSiniestros', 'sp_XMLAsientosPru')
  AND type = 'P';
