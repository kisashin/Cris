--liquibase formatted sql
--changeset j36147:HU_Reaseguro_566_Socios_Prod_Siniestros_20260903_01 stripComments:false dbms:mssql

USE [CardifWP]

GO
SET ANSI_NULLS ON
SET QUOTED_IDENTIFIER ON
GO

IF NOT EXISTS (SELECT 1 FROM dbo.Socios_Prod_Siniestros WHERE PRODUCTO = 2011)
    INSERT INTO dbo.Socios_Prod_Siniestros (PRODUCTO, REF_TRANSACCION, DESCRIPCION, NIT, RAMO, PK, X100_SOBREPRIMA)
    VALUES (2011, 'Aceptaciones reaseguro', 'Varios', '9999999999', 34, 832, NULL)

IF NOT EXISTS (SELECT 1 FROM dbo.Socios_Prod_Siniestros WHERE PRODUCTO = 2012)
    INSERT INTO dbo.Socios_Prod_Siniestros (PRODUCTO, REF_TRANSACCION, DESCRIPCION, NIT, RAMO, PK, X100_SOBREPRIMA)
    VALUES (2012, 'Aceptaciones reaseguro P', 'Varios', '9999999999', 34, NULL, NULL)

IF NOT EXISTS (SELECT 1 FROM dbo.Socios_Prod_Siniestros WHERE PRODUCTO = 2014)
    INSERT INTO dbo.Socios_Prod_Siniestros (PRODUCTO, REF_TRANSACCION, DESCRIPCION, NIT, RAMO, PK, X100_SOBREPRIMA)
    VALUES (2014, 'Aceptaciones reaseguro P', 'Varios', '9999999999', 34, NULL, NULL)

--rollback DELETE FROM dbo.Socios_Prod_Siniestros WHERE PRODUCTO IN (2011,2012,2014)
