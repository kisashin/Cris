SELECT c.name, t.name AS tipo, c.max_length, c.precision, c.scale
FROM sys.columns c
JOIN sys.types t ON t.user_type_id = c.user_type_id
WHERE c.object_id = OBJECT_ID('cardifwp.dbo.CUENTAS_CONTABLES_PROD')
  AND c.name IN ('TIPODIARIO','CUENTA','NATURALEZA','REF_TRANSACCION','Formula','Iva','id');
