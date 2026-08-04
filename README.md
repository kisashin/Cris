CREATE PROCEDURE [dbo].[sp_CargaSiniestros] (@Producto nvarchar(10)=null)
AS
BEGIN
declare @patron nvarchar(20),@Campos int,@sql nvarchar(4000),@C varchar(4),@socio nvarchar(10),@tparchivo nvarchar(10),@Insert nvarchar(4000)
--select @patron=case @Producto when 2005 then '326CO21SR02' end 
select @patron=(select patron from dbo.PatronxProd_siniestros where producto = @Producto)
Declare @Archivo as nvarchar(200),@cmd nvarchar(500),@j int,@Ruta nvarchar(100),@bulk nvarchar(500),@fechasistema nvarchar(15);

set @tparchivo='SINI'
set @sql=''
set @Ruta='d:\CargueSocios\Entrada\';
select @cmd='dir /B '+@Ruta+@patron+'*.csv'
create table #tmp(AR nvarchar(255));
insert into #tmp exec xp_cmdshell @cmd
delete  #tmp where isnull(ar,'File Not Found') like '%File Not%';
set @j=0;
select @j=count(*) from #tmp;
set @Insert=''

if @j>0 
Begin

set @C=1

select @Campos=max(idCampo) from configuracion_carguesocios where producto=@Producto and tipo_Archivo=@tparchivo
set @sql='create table ##tmpCargaSiniestros ('

while cast(@C as float)<=@Campos
	begin
		set @sql=@sql+'C'+@C+' nvarchar(100),'
		set @Insert=@Insert+'C'+@C+',';
			set @C=@C+1;
	end

set @sql=@sql+ '&)'
set @sql=replace (@sql,',&)',')')
set @insert =@insert+ '&'
set @insert =replace (@insert,',&','')

exec (@Sql);

	declare tAR cursor for  	select * from #tmp;
	open tAR;
	fetch next from  tAR into @Archivo;
	while @@fetch_status=0
	begin
		set @bulk='bulk insert ##tmpCargaSiniestros
		from '+char(39)+@Ruta+@Archivo
		+char(39)+ ' with (fieldterminator='+char(39)+';'+char(39)+', rowterminator=' +char(39)+'\n'+char(39)+')'
		--print @bulk
		exec (@bulk)

		select @fechasistema=dbo.Ffecha2txt(getdate(),'')
	select top 1 @socio=socio from configuracion_carguesocios where producto=@producto and tipo_archivo=@tparchivo

		delete from CargueSociosSiniestros where NombreArchivo=@Archivo and producto=@Producto and tpArchivo=@tparchivo
	set @sql=''
	set @sql='insert into CargueSociosSiniestros (socio,Producto, tparchivo, fecha_sistema, NombreArchivo, EstadoReg,'+@Insert+')
	select '+@socio+','+@Producto+','+char(39)+ @tparchivo +char(39)+','+char(39)+ @fechasistema +char(39)+','+char(39)+ @Archivo + char(39)+','+char(39)+'OK' +char(39)+ ',* from ##tmpCargaSiniestros';
	
	exec (@sql)

		set @cmd='move '+@Ruta+@Archivo+' '+@Ruta+'\Procesados\'+@Archivo
		exec xp_cmdshell @cmd, no_output 
		fetch next from  tAR into @Archivo;
	end;
	close tAR;
	deallocate tAR;
	select cast(count(*) as nvarchar(20)) +' Registros Cargados : '+@Archivo from ##tmpCargaSiniestros
	drop table ##tmpCargaSiniestros

End

Else select 'No hay archivo de siniestros'--+@cmd;

END









GO
