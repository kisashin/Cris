USE CardifWP;

SELECT 'CargueSociosSiniestros' AS objeto, OBJECT_ID('dbo.CargueSociosSiniestros') AS id
UNION ALL
SELECT 'configuracion_carguesocios', OBJECT_ID('dbo.configuracion_carguesocios');

SELECT producto, tipo_Archivo, MAX(idCampo) AS campos
FROM configuracion_carguesocios
WHERE producto IN (2011, 2012, 2014, 2020, 2028)
GROUP BY producto, tipo_Archivo;
