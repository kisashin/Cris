USE SiniestrosWp;
GO
SET LOCK_TIMEOUT 5000;
ALTER TABLE dbo.tmpsiniestros_ext ALTER COLUMN [Cobertura_afectada ] nvarchar(255) NULL;
GO
