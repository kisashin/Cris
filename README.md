SELECT
    OBJECT_SCHEMA_NAME(d.referencing_id) AS EsquemaOrigen,
    OBJECT_NAME(d.referencing_id) AS ProcedimientoOrigen,
    d.referenced_schema_name AS EsquemaReferenciado,
    d.referenced_entity_name AS ObjetoReferenciado,
    d.referenced_database_name AS BaseReferenciada
FROM sys.sql_expression_dependencies d
WHERE OBJECT_NAME(d.referencing_id) IN (
    'sp_Genera_Datos_Siniestros',
    'SP_Reporte_Datos_Siniestros',
    'SP_Reporte_Movimientos_Siniestros'
)
ORDER BY ProcedimientoOrigen, ObjetoReferenciado;
