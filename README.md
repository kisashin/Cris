SELECT COUNT(*) AS filas FROM SiniestrosWp.dbo.tmpsiniestros_ext;

SET ARITHABORT OFF;
SET ANSI_WARNINGS ON;
SET ANSI_NULLS ON;
SET CONCAT_NULL_YIELDS_NULL ON;
GO
EXEC dbo.sp_contabiliza_cardif_ext;
