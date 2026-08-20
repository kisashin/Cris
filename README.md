-- ¿IDCARVAJAL es identity en historicomovimientos_ext? Si no lo es, hay que darle valor
SELECT c.name, c.is_identity, c.is_nullable, t.name AS tipo
FROM sys.columns c JOIN sys.types t ON t.user_type_id = c.user_type_id
WHERE c.object_id = OBJECT_ID('dbo.historicomovimientos_ext')
  AND c.name IN ('IDCARVAJAL','id','Fechamovimiento2','Ramo','Vrmovimiento');

-- ¿Qué valores de IVA tienen las 14 cuentas? Define qué Ramo sirve
SELECT IVA, COUNT(*) FROM cardifwp.dbo.CUENTAS_CONTABLES_PROD
WHERE GRUPO='RE' AND TIPODIARIO IN ('CRVSI','LRVSI','SINIE') GROUP BY IVA;

