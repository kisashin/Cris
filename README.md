SELECT OBJECT_NAME(object_id) AS SP, definition
FROM sys.sql_modules
WHERE object_id IN (
    OBJECT_ID('dbo.sp_CargaSiniestrosAlfa'),
    OBJECT_ID('dbo.sp_CargaSiniestros'),
    OBJECT_ID('dbo.sp_XMLAsientosPru')
);
