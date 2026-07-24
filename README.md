SELECT
    SCHEMA_NAME(schema_id) AS Esquema,
    name AS Procedimiento,
    create_date AS FechaCreacion,
    modify_date AS FechaModificacion
FROM sys.procedures
WHERE name IN (
    'sp_Genera_Datos_Siniestros',
    'SP_Reporte_Datos_Siniestros',
    'SP_Reporte_Movimientos_Siniestros'
);


SELECT DB_NAME() AS BaseDatosActual;


SELECT
    SCHEMA_NAME(p.schema_id) AS Esquema,
    p.name AS Procedimiento,
    sm.definition AS CodigoSQL
FROM sys.procedures p
INNER JOIN sys.sql_modules sm
    ON p.object_id = sm.object_id
WHERE p.name IN (
    'sp_Genera_Datos_Siniestros',
    'SP_Reporte_Datos_Siniestros',
    'SP_Reporte_Movimientos_Siniestros'
)
ORDER BY p.name;


EXEC sp_helptext 'dbo.sp_Genera_Datos_Siniestros';

EXEC sp_helptext 'dbo.SP_Reporte_Datos_Siniestros';

EXEC sp_helptext 'dbo.SP_Reporte_Movimientos_Siniestros';


SELECT
    SCHEMA_NAME(o.schema_id) AS Esquema,
    o.name AS Procedimiento,
    p.parameter_id,
    p.name AS Parametro,
    TYPE_NAME(p.user_type_id) AS TipoDato,
    p.max_length,
    p.precision,
    p.scale,
    p.is_output
FROM sys.objects o
LEFT JOIN sys.parameters p
    ON o.object_id = p.object_id
WHERE o.type = 'P'
  AND o.name IN (
      'sp_Genera_Datos_Siniestros',
      'SP_Reporte_Datos_Siniestros',
      'SP_Reporte_Movimientos_Siniestros'
  )
ORDER BY o.name, p.parameter_id;


EXEC sp_help 'dbo.TBL_Archivo_Datos';

EXEC sp_help 'dbo.TBL_Historico_Movimientos';

EXEC sp_help 'dbo.tbl_historico_inicial';

SELECT TOP 10 *
FROM dbo.TBL_Archivo_Datos
ORDER BY id DESC;

SELECT TOP 10 *
FROM dbo.TBL_Historico_Movimientos;

SELECT TOP 10 *
FROM dbo.tbl_historico_inicial;


SELECT DISTINCT
    H1.Llavesiniestro AS Llavesiniestros
FROM dbo.TBL_Historico_Movimientos H1
LEFT JOIN dbo.tbl_historico_inicial H2
    ON H1.Llavesiniestro = H2.Llavesiniestro
WHERE H2.Llavesiniestro IS NULL;
