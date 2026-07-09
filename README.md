-- ¿de qué periodo son los datos de cada una? (usa una fecha que exista en el layout)
SELECT 'CardifWP' AS base, MIN(Fecha_aviso_Cardif) AS desde, MAX(Fecha_aviso_Cardif) AS hasta
FROM CardifWP.dbo.tmpSiniestros
UNION ALL
SELECT 'SiniestrosWp', MIN(Fecha_aviso_Cardif), MAX(Fecha_aviso_Cardif)
FROM SiniestrosWp.dbo.tmpSiniestros;
