USE CardifWP;
SELECT OBJECT_NAME(object_id) AS objeto, definition
FROM sys.sql_modules
WHERE object_id IN (
  OBJECT_ID('dbo.sp_XMLAsientosPru'),              -- 1: corazón (SINIE/LRVSI/CRVSI + bcp?)
  OBJECT_ID('dbo.sp_AsientoSiniestrosAdicionales'),-- 2: nombres exactos de columnas modos 1 y 3
  OBJECT_ID('dbo.sp_CargaSiniestros'),             -- 3: ¿mensaje inline o de tabla?
  OBJECT_ID('dbo.sp_CargaSiniestrosAlfa'),
  OBJECT_ID('dbo.ListaArhivos'),                   -- 4: ¿Database Mail o solo registro?
  OBJECT_ID('dbo.fFecha2Txt'),                     -- 5: formato fecha (define el substring del front)
  OBJECT_ID('dbo.truncdate')
);
