--liquibase formatted sql

--changeset j36147:HU_DDPT_XXX_20260909_1 stripComments:false dbms:mssql
UPDATE SiniestrosWp.dbo.CUENTAS_CONTABLES_PROD
SET CUENTA = '41164501'
WHERE id = 1159
  AND GRUPO = 'HOGAR'
  AND TIPODIARIO = 'SIREA'
  AND Formula = 'vTerremoto'
  AND CUENTA = '41165401'
--rollback UPDATE SiniestrosWp.dbo.CUENTAS_CONTABLES_PROD SET CUENTA = '41165401' WHERE id = 1159 AND GRUPO = 'HOGAR' AND TIPODIARIO = 'SIREA' AND Formula = 'vTerremoto' AND CUENTA = '41164501'
