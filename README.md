USE CardifWP;

SELECT COLUMN_NAME, DATA_TYPE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'CargaSiniestrosAlfa'
  AND COLUMN_NAME IN ('AVISOS','PAGO_DEFINITIVO','RES_ANTERIOR','LIBERACIONES_rebajas');


  SELECT OBJECT_NAME(referencing_id) AS usa_fFloat
FROM sys.sql_expression_dependencies
WHERE referenced_entity_name = 'fFloat';
