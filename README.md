USE SiniestrosWp;

SELECT c.column_id, c.name, TYPE_NAME(c.user_type_id) AS tipo, c.max_length,
       c.precision, c.scale, c.is_nullable, c.is_identity
FROM sys.columns c WHERE c.object_id = OBJECT_ID('dbo.historicomovimientos')
ORDER BY c.column_id;

SELECT c.column_id, c.name, TYPE_NAME(c.user_type_id) AS tipo, c.max_length,
       c.precision, c.scale, c.is_nullable, c.is_identity
FROM sys.columns c WHERE c.object_id = OBJECT_ID('dbo.novedadhistoricoindividual')
ORDER BY c.column_id;

SELECT OBJECT_NAME(i.object_id) AS tabla, i.name AS indice, i.is_primary_key,
       i.is_unique, c.name AS columna, ic.key_ordinal
FROM sys.indexes i
JOIN sys.index_columns ic ON ic.object_id = i.object_id AND ic.index_id = i.index_id
JOIN sys.columns c ON c.object_id = i.object_id AND c.column_id = ic.column_id
WHERE i.object_id IN (OBJECT_ID('dbo.historicomovimientos'),
                      OBJECT_ID('dbo.novedadhistoricoindividual'))
ORDER BY i.object_id, i.index_id, ic.key_ordinal;


--liquibase formatted sql
--changeset j36147:HU_DDPT_566_20260810_2 stripComments:false dbms:mssql
USE [SiniestrosWp]
GO
DELETE FROM [dbo].[tbl_Archivo_socios]
WHERE [idArchivosocios_cen] IN (2, 3);
GO


