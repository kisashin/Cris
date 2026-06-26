EXEC sp_helptext 'dbo.sp_contabiliza_cardifCentro';

SELECT name, type_name(user_type_id) AS tipo
FROM sys.parameters
WHERE object_id = OBJECT_ID('dbo.sp_contabiliza_cardifCentro');
