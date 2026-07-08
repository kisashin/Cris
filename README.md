-- ¿Cuál tmpSiniestros tiene datos ahora mismo?
SELECT 'CardifWP' AS base, COUNT(*) AS filas FROM CardifWP.dbo.tmpSiniestros
UNION ALL
SELECT 'SiniestrosWp', COUNT(*) FROM SiniestrosWp.dbo.tmpSiniestros;
