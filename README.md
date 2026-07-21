USE CardifWP;
GO

--exec sp_CargaSiniestrosAlfa
ALTER PROCEDURE [dbo].[sp_CargaSiniestrosAlfa] (@Producto int=null)
AS
BEGIN
declare @patron nvarchar(20)
--select @patron=case @Producto when 2005 then '326CO21SR02' end
select @patron=(select patron from dbo.PatronxProd_siniestros where producto = @Producto)

		Declare @Archivo as nvarchar(200),@cmd nvarchar(500),@j int,@Ruta nvarchar(100),@bulk nvarchar(500);

--set @Ruta='d:\CargueSocios\Entrada\';
set @Ruta='d:\CargueSocios\SALIDA\XML\';
select @cmd='dir /B '+@Ruta+@patron+'*.csv'
create table #tmp(AR nvarchar(255));
insert into #tmp exec xp_cmdshell @cmd
delete  #tmp where isnull(ar,'File Not Found') like '%File Not%';
set @j=0;
select @j=count(*) from #tmp;
if @j>0
Begin
	delete from tmpCargaSiniestrosAlfa
	--print @cmd;
	declare tAR cursor for
	select * from #tmp;
	open tAR;
	fetch next from  tAR into @Archivo;
	while @@fetch_status=0
	begin
		set @bulk='bulk insert dbo.tmpCargaSiniestrosAlfa
		from '+char(39)+@Ruta+@Archivo
		+char(39)+ ' with (fieldterminator='+char(39)+';'+char(39)+', rowterminator=' +char(39)+'\n'+char(39)+')'
		--print @bulk
		exec (@bulk)

		delete from tmpCargaSiniestrosAlfa where ramo='Ramo' or suc='suc' or poliza='Poliza' or siniestro='siniestro'
		update tmpCargaSiniestrosAlfa set RES_ANTERIOR=0 where RES_ANTERIOR like '%-%'
		update tmpCargaSiniestrosAlfa set AVISOS=0 where AVISOS like '%-%'
		update tmpCargaSiniestrosAlfa set PAGO_DEFINITIVO=0 where PAGO_DEFINITIVO like '%-%'
		update tmpCargaSiniestrosAlfa set SOBREPAGO=0 where SOBREPAGO like '%-%'
		update tmpCargaSiniestrosAlfa set LIBERACIONES_rebajas=0 where LIBERACIONES_rebajas like '%-%'
		update tmpCargaSiniestrosAlfa set INCREMENTOS=0 where INCREMENTOS like '%-%'
		update tmpCargaSiniestrosAlfa set CANCELACIONES_liberaciones=0 where CANCELACIONES_liberaciones like '%-%'
		update tmpCargaSiniestrosAlfa set REVERSIONES=0 where REVERSIONES like '%-%'
		update tmpCargaSiniestrosAlfa set RES_ACTUAL=0 where RES_ACTUAL like '%-%'
		update tmpCargaSiniestrosAlfa set RECUP_PAGOS=0 where RECUP_PAGOS like '%-%'
		update tmpCargaSiniestrosAlfa set VLR_RECLAMO=0 where VLR_RECLAMO like '%-%'
		update tmpCargaSiniestrosAlfa set VLR_DESEMBOLSO=0 where VLR_DESEMBOLSO like '%-%'

-- Deben venir 2 decimales

		update tmpCargaSiniestrosAlfa set RES_ANTERIOR=RES_ANTERIOR+'0' where substring(right(RES_ANTERIOR,2),1,1)=','
		update tmpCargaSiniestrosAlfa set AVISOS=AVISOS+'0' where substring(right(AVISOS,2),1,1)=','
		update tmpCargaSiniestrosAlfa set PAGO_DEFINITIVO=PAGO_DEFINITIVO+'0' where substring(right(PAGO_DEFINITIVO,2),1,1)=','
		update tmpCargaSiniestrosAlfa set SOBREPAGO=SOBREPAGO+'0' where substring(right(SOBREPAGO,2),1,1)=','
		update tmpCargaSiniestrosAlfa set LIBERACIONES_rebajas=LIBERACIONES_rebajas+'0' where substring(right(LIBERACIONES_rebajas,2),1,1)=','
		update tmpCargaSiniestrosAlfa set INCREMENTOS=INCREMENTOS+'0' where substring(right(INCREMENTOS,2),1,1)=','
		update tmpCargaSiniestrosAlfa set CANCELACIONES_liberaciones=CANCELACIONES_liberaciones+'0' where substring(right(CANCELACIONES_liberaciones,2),1,1)=','
		update tmpCargaSiniestrosAlfa set REVERSIONES=REVERSIONES+'0' where substring(right(REVERSIONES,2),1,1)=','
		update tmpCargaSiniestrosAlfa set RES_ACTUAL=RES_ACTUAL+'0' where substring(right(RES_ACTUAL,2),1,1)=','
		update tmpCargaSiniestrosAlfa set RECUP_PAGOS=RECUP_PAGOS+'0' where substring(right(RECUP_PAGOS,2),1,1)=','
		update tmpCargaSiniestrosAlfa set VLR_RECLAMO=VLR_RECLAMO+'0' where substring(right(VLR_RECLAMO,2),1,1)=','
		update tmpCargaSiniestrosAlfa set VLR_DESEMBOLSO=VLR_DESEMBOLSO+'0' where substring(right(VLR_DESEMBOLSO,2),1,1)=','


/*
		update tmpCargaSiniestrosAlfa set RES_ANTERIOR=DBO.FFLOAT(RES_ANTERIOR)
		update tmpCargaSiniestrosAlfa set avisos=DBO.FFLOAT(avisos)
		update tmpCargaSiniestrosAlfa set PAGO_DEFINITIVO=DBO.FFLOAT(PAGO_DEFINITIVO)
		update tmpCargaSiniestrosAlfa set SOBREPAGO=DBO.FFLOAT(SOBREPAGO)
		update tmpCargaSiniestrosAlfa set LIBERACIONES_rebajas=DBO.FFLOAT(LIBERACIONES_rebajas)
		update tmpCargaSiniestrosAlfa set INCREMENTOS=DBO.FFLOAT(INCREMENTOS)
		update tmpCargaSiniestrosAlfa set CANCELACIONES_liberaciones=DBO.FFLOAT(CANCELACIONES_liberaciones)
		update tmpCargaSiniestrosAlfa set REVERSIONES= DBO.FFLOAT(REVERSIONES)
		update tmpCargaSiniestrosAlfa set RES_ACTUAL= DBO.FFLOAT(RES_ACTUAL)
		update tmpCargaSiniestrosAlfa set RECUP_PAGOS= DBO.FFLOAT(RECUP_PAGOS)
		update tmpCargaSiniestrosAlfa set VLR_RECLAMO= DBO.FFLOAT(VLR_RECLAMO)
		update tmpCargaSiniestrosAlfa set VLR_DESEMBOLSO=DBO.FFLOAT(VLR_DESEMBOLSO)
*/

	/*
		if (select count(*) from CargaSiniestrosAlfa where producto=@producto)>0
		begin
			declare @ReservaAnterior float
			declare @ReservaActual float
			select @ReservaAnterior=sum(RES_ACTUAL) from CargaSiniestrosAlfa where NombreArchivo=(select top 1 nombrearchivo
						from CargaSiniestrosAlfa where producto=@producto and FechaProceso=(select max(FechaProceso)from dbo.CargaSiniestrosAlfa where producto=@producto))

			select @ReservaActual=sum(DBO.FFLOAT(RES_ANTERIOR)) from tmpCargaSiniestrosAlfa

			if (@ReservaActual <>@ReservaAnterior)
				begin
				select 'Reserva anterior no coincide en el archivo: '+@Archivo
				return
				end
		end
		*/

		delete from CargaSiniestrosAlfa where NombreArchivo=@Archivo --and dbo.truncdate(fechaProceso)= dbo.truncdate(getdate())
		insert into CargaSiniestrosAlfa
		SELECT [NoRAMO] ,[RAMO],[SINIESTRO],[T_PAGO],[SUC] ,[SIMB],[POLIZA],[VIG] ,[ASEGURADO] ,[CC_ASEGURADO]
      ,[TOMADOR] ,DBO.FFLOAT(RES_ANTERIOR) ,DBO.FFLOAT(avisos),DBO.FFLOAT(PAGO_DEFINITIVO) ,DBO.FFLOAT(SOBREPAGO) ,DBO.FFLOAT(LIBERACIONES_rebajas) ,DBO.FFLOAT(INCREMENTOS)
      ,DBO.FFLOAT(CANCELACIONES_liberaciones) ,DBO.FFLOAT(REVERSIONES) ,DBO.FFLOAT(RES_ACTUAL) ,DBO.FFLOAT(RECUP_PAGOS) ,[FECHA_PAGO]  ,[LIDER]
      ,[FECHA_STRO] ,[FECHA_AVISO] ,[FECHA_RECLAMO] ,[REPORTADO] ,DBO.FFLOAT(VLR_RECLAMO) ,[DESCRIPCION]  ,[CAUSA] ,[LUGAR]
      ,[OBSERVACIONES] ,[CREDITO] ,DBO.FFLOAT(VLR_DESEMBOLSO) ,[FECHA_DESEMB] ,[PORCASEGU] ,[GENERO],[EDAD] ,[LINEA_DE_CREDITO]
      ,[USUARIO_RES] ,[USUARIO_ANALIS] ,[USUARIO_PAGO] ,[COD_AJUSTADOR] ,[FECHA_OBJECION] ,[PERFIL]  ,[ESTADO]
		,@Archivo,getdate(),@producto
		FROM [CardifWP].[dbo].[tmpCargaSiniestrosAlfa]

		set @cmd='move '+@Ruta+@Archivo+' '+@Ruta+'\Procesados\'+@Archivo
		exec xp_cmdshell @cmd, no_output

		fetch next from  tAR into @Archivo;
	end;
	close tAR;
	deallocate tAR;
	select cast(count(*) as nvarchar(20)) +' Registros Cargados : '+@Archivo from tmpCargaSiniestrosAlfa

End

Else select 'No hay archivo de siniestros'--+@cmd;

END
GO
