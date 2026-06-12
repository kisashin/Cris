EXEC sp_help 'dbo.reportecontable_peru';

SELECT
    COLUMN_NAME,
    DATA_TYPE,
    CHARACTER_MAXIMUM_LENGTH,
    NUMERIC_PRECISION,
    NUMERIC_SCALE,
    IS_NULLABLE,
    ORDINAL_POSITION
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'dbo'
  AND TABLE_NAME = 'reportecontable_peru'
ORDER BY ORDINAL_POSITION;

EXEC sp_helptext 'dbo.SP_ReporteContablePeru';

SELECT OBJECT_DEFINITION(
    OBJECT_ID('dbo.SP_ReporteContablePeru')
);


SELECT COUNT(*) AS TotalRecords
FROM dbo.reportecontable_peru;

SELECT TOP 5 *
FROM dbo.reportecontable_peru;
