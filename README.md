USE CardifWP;
SELECT OBJECT_NAME(referencing_id) AS llamador
FROM sys.sql_expression_dependencies
WHERE referenced_entity_name = 'sp_XMLAsientosPru';
