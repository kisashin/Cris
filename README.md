-- ============================================================
-- 1. EL CUERPO DEL SP (esto es lo que más duda cierra, no es "consulta" pero es SQL)
--    Correr en SiniestrosWp. Devuelve celda, doble-clic la abre limpia.
--    Con esto veo: en qué MODOS cruza a CardifWP y en cuáles no.
-- ============================================================
SELECT OBJECT_DEFINITION(OBJECT_ID('dbo.sp_asientosSiniestros'));
-- (ya lo tienes de antes pero llegó mutilado por sp_helptext; este sale limpio)

-- ============================================================
-- 2. ¿ListaArhivos cruza a CardifWP? (para saber si el correo va en tu lado o el otro)
--    Correr en SiniestrosWp
-- ============================================================
SELECT OBJECT_DEFINITION(OBJECT_ID('dbo.ListaArhivos'));

-- ============================================================
-- 3. Confirmar que los catálogos SÍ viven solo en CardifWP y no hay copia en SiniestrosWp
--    (si existieran en ambas, no habría cross-database y todo cambia)
--    Correr UNA vez, desde cualquier base
-- ============================================================
SELECT 'CardifWP' AS base, name FROM CardifWP.sys.objects
WHERE name IN ('producto_td_cierre','prp')
UNION ALL
SELECT 'SiniestrosWp', name FROM SiniestrosWp.sys.objects
WHERE name IN ('producto_td_cierre','prp');
