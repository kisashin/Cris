ALTER procedure  [dbo].[sp_Gen_Xml_Siniestros_Reaseg_Ext](@FC nvarchar(6)) as   
BEGIN
	SET ARITHABORT ON;
	
	declare @corte datetime=@FC+'01';
	...

  SET ARITHABORT OFF;
GO
EXEC dbo.sp_contabiliza_cardif_ext;
