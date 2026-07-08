SELECT 'CardifWP' AS base, name, type_desc
FROM CardifWP.sys.objects
WHERE name IN ('tmpSiniestros','historicoasientospru','Parametro',
               'sp_asientosSiniestros','sp_XMLAsientosPru','ListaArhivos')
UNION ALL
SELECT 'SiniestrosWp' AS base, name, type_desc
FROM SiniestrosWp.sys.objects
WHERE name IN ('tmpSiniestros','historicoasientospru','Parametro',
               'sp_asientosSiniestros','sp_XMLAsientosPru','ListaArhivos');
