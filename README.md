--liquibase formatted sql
--changeset j36147:HU_Reaseguro_566_Cobertura_2011_20260914_01 stripComments:false dbms:mssql

USE [CardifWP]

GO
SET ANSI_NULLS ON
SET QUOTED_IDENTIFIER ON
GO

IF NOT EXISTS (SELECT 1 FROM dbo.Cobertura_Prod_Xpln_Plz_Cnl WHERE PRODUCTO = '2011' AND COBERTURA = 'INCAP.PERM.TOT.')
    INSERT INTO dbo.Cobertura_Prod_Xpln_Plz_Cnl (PRODUCTO, AFECTADOX, VALOR, COBERTURA, PESO, RAMO, IVA, PK, APPS, COD_COBERT_ACSELE, Nombre_comercial_de_la_cobertura)
    VALUES ('2011', '0', '0', 'INCAP.PERM.TOT.', 0.27, 34, 0, NULL, NULL, 701, NULL)

IF NOT EXISTS (SELECT 1 FROM dbo.Cobertura_Prod_Xpln_Plz_Cnl WHERE PRODUCTO = '2011' AND COBERTURA = 'MUERTE')
    INSERT INTO dbo.Cobertura_Prod_Xpln_Plz_Cnl (PRODUCTO, AFECTADOX, VALOR, COBERTURA, PESO, RAMO, IVA, PK, APPS, COD_COBERT_ACSELE, Nombre_comercial_de_la_cobertura)
    VALUES ('2011', '0', '0', 'MUERTE', 0.73, 34, 0, NULL, NULL, 418, NULL)

--rollback DELETE FROM dbo.Cobertura_Prod_Xpln_Plz_Cnl WHERE PRODUCTO = '2011' AND COBERTURA IN ('INCAP.PERM.TOT.','MUERTE')
