-- ============================================================
-- A. UBICACIÓN: ¿qué vive en CardifWP y qué en SiniestrosWp?
--    Correr EN CardifWP Y EN SiniestrosWp por separado, comparar.
--    Donde devuelve número = existe ahí. Donde NULL = no está.
-- ============================================================
SELECT
  OBJECT_ID('dbo.tmpSiniestros')            AS tmpSiniestros,
  OBJECT_ID('dbo.historicoasientospru')     AS historicoasientospru,
  OBJECT_ID('dbo.Parametro')                AS Parametro,
  OBJECT_ID('dbo.sp_asientosSiniestros')    AS sp_asiento,
  OBJECT_ID('dbo.sp_XMLAsientosPru')        AS sp_xml,
  OBJECT_ID('dbo.ListaArhivos')             AS sp_correo,
  OBJECT_ID('dbo.tmpInterfazSiniestros_TEMP') AS tmp_interfaz,
  OBJECT_ID('dbo.Hitorico_Siniestros_InterfazContable') AS hist_interfaz;

-- ============================================================
-- B. CUERPO de los 3 SP que NO hemos visto completos.
--    NO uses sp_helptext (se parte). Devuelve celda, doble-clic la abre.
--    Correr en la base donde A los reporte no-null.
-- ============================================================
SELECT OBJECT_DEFINITION(OBJECT_ID('dbo.sp_asientosSiniestros'));  -- resuelve el hueco 3: qué modo lee vs escribe, y el bug if/print
SELECT OBJECT_DEFINITION(OBJECT_ID('dbo.sp_XMLAsientosPru'));      -- confirma generación real del XML
SELECT OBJECT_DEFINITION(OBJECT_ID('dbo.ListaArhivos'));           -- confirma si correo es paso o servicio aparte

-- ============================================================
-- C. ¿El usuario de la app puede alcanzar cross-database?
--    Esto es lo que truena en QA/prod. Correr conectado como 'dts'
--    (o el usuario real de la app) contra CardifWP.
-- ============================================================
SELECT SUSER_NAME() AS usuario_actual, DB_NAME() AS base_actual;
-- prueba de alcance real:
SELECT TOP 1 * FROM SiniestrosWp.dbo.Parametro;  -- si falla = no hay permiso cross-db = problema de ambiente
