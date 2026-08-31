--liquibase formatted sql

--changeset j36147:sp_contabiliza_cardif_pantalla stripComments:false dbms:mssql
USE [SiniestrosWp]

GO
SET ANSI_NULLS ON
SET QUOTED_IDENTIFIER ON
GO
CREATE OR ALTER PROCEDURE [dbo].[sp_contabiliza_cardif](@r int=null)--todo=null,Rev=1, Otros=2
AS
Declare
@fecha varchar(12),
@periodo varchar(12),
@mes1 int,
@mes2 varchar(2),
@ano1 int,
@ano2 varchar(4),
@periodohogar varchar(12),
@nombre varchar(40)


BEGIN
SET NOCOUNT ON

create table #salidaXml(
 Familia varchar(50),
 Periodo nvarchar(6),
 Pasada int,
 Mv varchar(50),
 NombreArchivo nvarchar(100),
 Secuencia bigint,
 Line nvarchar(max))

create table #reaseg(
 Familia varchar(50),
 Periodo nvarchar(6),
 Mv varchar(50),
 Secuencia bigint,
 Line nvarchar(max))

create table #directas(
 Tipo_Diario varchar(50),
 NombreArchivo nvarchar(100),
 Contenido nvarchar(max))

create table #asientos(Registrado nvarchar(max))

select top 1 @fecha = CONVERT(nvarchar(8),fecha,112) from controlcierreaval

select @mes2 = substring(@fecha,5,2)
select @ano2 = substring(@fecha,1,5)
select @mes1 = cast(@mes2 as int)
select @ano1 = cast(@ano2 as int)
--select @nombre = case isnull(@r,0) when 1 then 'rv' else '' end +'ASSE' + @fecha + '_CAR'
select @nombre = 'ASSE' + @fecha + '_CAR'
select @periodo = @ano2 + '/0' + @mes2
select @periodohogar = @ano2 + @mes2


------------if @r is null
------------begin
------------	exec sp_contabiliza_cardif 2 --Otros mv
------------	exec sp_contabiliza_cardif 1 --mv Rever
------------	return 0
------------end


delete from SiniestrosWp.dbo.tmpsiniestros

------------if 1<>@r
------------begin

	-- Aumentos

	insert into SiniestrosWp.dbo.tmpsiniestros(Numero_radicacion_siniestro,Doc_Asegurado,
	Cobertura_afectada,cod_producto,cod_plan,Ramo,Fecha_aviso_Cardif,Reserva_inicial_constituida,Nombre_asegurado,Poliza,id2)
	Select NumeroSiniestro as Numero_radicacion_siniestro,
	NroIdentificacion as Doc_Asegurado,
	Cobertura as Cobertura_afectada ,
	CodProducto as cod_producto,
	case when isnumeric(CodPlan)=0 then '0' when isnumeric(CodPlan)>0 and CodPlan > 9 then '0' else isnull(CodPlan,'0') end as cod_plan ,
	Ramo,
	FechaMovimiento2 as Fecha_aviso_Cardif,
	VrMovimiento as  Reserva_inicial_constituida,upper(left(ltrim(rtrim(Nombreasegurado)),50)),null, id
	from historicomovimientos (nolock) where
	tipoMovimiento in('Aumento Reserva','Reserva Inicial - Aseguradora')
	and llavesiniestro in (select llavesiniestro from historico_inicial where Aval = 0) 
	and fechacontabilizacion is null
	--and year(FechaMovimiento2)=2016 and month(FechaMovimiento2)=8 
	


	--Pagos

	insert into SiniestrosWp.dbo.tmpsiniestros(Numero_radicacion_siniestro,Doc_Asegurado,Cobertura_afectada,cod_producto,cod_plan,Ramo,
	Fecha_pago_cuota1,cuota1,Nombre_asegurado,Poliza,id2,[Nombre_beneficiario ],Resultado_siniestro,Num_Planilla)
	Select NumeroSiniestro as Numero_radicacion_siniestro,
	NroIdentificacion as Doc_Asegurado,
	Cobertura as Cobertura_afectada ,
	CodProducto as cod_producto,
	case when isnumeric(CodPlan)=0 then '0' when isnumeric(CodPlan)>0 and CodPlan > 9 then '0' else isnull(CodPlan,'0') end as cod_plan ,
	Ramo,
	FechaMovimiento2 as Fecha_pago_cuota1,
	VrMovimiento as  cuota1,upper(left(ltrim(rtrim(Nombreasegurado)),50)),null, id,
	upper(left(ltrim(rtrim(Beneficiariopago)),60)),NumeroIdentificacionBeneficiarioDelPago,Iddoctosoportemanutencion
	from historicomovimientos (nolock) where 
	tipoMovimiento in('Pago')
	and llavesiniestro in (select llavesiniestro from historico_inicial where Aval = 0) 
	and fechacontabilizacion is null
	--and year(FechaMovimiento2)=2016 and month(FechaMovimiento2)=8 
	

	--Disminuciones

	insert into SiniestrosWp.dbo.tmpsiniestros(Numero_radicacion_siniestro,Doc_Asegurado,Cobertura_afectada,cod_producto,cod_plan,Ramo,
	Fecha_dismi_reserva,Valor_dismin_reserva,Nombre_asegurado,Poliza,id2)
	Select NumeroSiniestro as Numero_radicacion_siniestro,
	NroIdentificacion as Doc_Asegurado,
	Cobertura as Cobertura_afectada ,
	CodProducto as cod_producto,
	case when isnumeric(CodPlan)=0 then '0' when isnumeric(CodPlan)>0 and CodPlan > 9 then '0' else isnull(CodPlan,'0') end as cod_plan ,
	Ramo,
	FechaMovimiento2 as Fecha_dismi_reserva,
	VrMovimiento as  Valor_dismin_reserva,upper(left(ltrim(rtrim(Nombreasegurado)),50)),null, id
	from historicomovimientos (nolock) where 
	tipoMovimiento in('Disminución Reserva','Objetado','Anulado ','Anulado','Disminucion Reserva','objecion')
	and llavesiniestro in (select llavesiniestro from historico_inicial where Aval = 0) 
	and fechacontabilizacion is null
	--and year(FechaMovimiento2)=2016 and month(FechaMovimiento2)=8 
	

	--GENERA LOS XML DE REASEGURO CARDIF RAMO 22
	delete from #reaseg
	insert into #reaseg exec sp_Gen_Xml_Siniestros_ReasegCardif @periodohogar

	insert into #salidaXml(Familia,Periodo,Pasada,Mv,NombreArchivo,Secuencia,Line)
	select Familia,Periodo,1,Mv,null,Secuencia,Line from #reaseg

	---ESTE NO GENERA XML'S
	insert into #asientos exec SiniestrosWp.dbo.sp_asientosSiniestros @ano1,@mes1,4,@nombre

	--ESTE GENERA LOS XML DE DIRECTAS NORMAL SIN LOS DE REVERSA GENERA 3 XML
	delete from #directas
	insert into #directas exec SiniestrosWp.dbo.sp_XMLAsientosPru 'SINIE',@periodo,null,@nombre,'PANTALLA'
	insert into #directas exec SiniestrosWp.dbo.sp_XMLAsientosPru 'LRVSI',@periodo,null,@nombre,'PANTALLA'
	insert into #directas exec SiniestrosWp.dbo.sp_XMLAsientosPru 'CRVSI',@periodo,null,@nombre,'PANTALLA'

	insert into #salidaXml(Familia,Periodo,Pasada,Mv,NombreArchivo,Secuencia,Line)
	select 'Directas',@periodohogar,1,Tipo_Diario,NombreArchivo,1,Contenido
	from #directas where Contenido is not null


--print 'entro'
--end

--------if 1=@r
--------begin
-- Reversa 1  Pagos(Disminuciones)



	select @nombre = 'rvASSE' + @fecha + '_CAR'

	delete from SiniestrosWp.dbo.tmpsiniestros


	insert into SiniestrosWp.dbo.tmpsiniestros(Numero_radicacion_siniestro,Doc_Asegurado,Cobertura_afectada,cod_producto,cod_plan,Ramo,
	fecha_dismi_reserva,Valor_dismin_reserva,Fecha_pago_cuota1,cuota1,Nombre_asegurado,Poliza,id2
	,[Nombre_beneficiario ],Resultado_siniestro, Num_planilla)
	Select NumeroSiniestro as Numero_radicacion_siniestro,
	NroIdentificacion as Doc_Asegurado,
	Cobertura as Cobertura_afectada ,
	CodProducto as cod_producto,
	case when isnumeric(CodPlan)=0 then '0' when isnumeric(CodPlan)>0 and CodPlan > 9 then '0' else isnull(CodPlan,'0') end as cod_plan ,
	Ramo,
	--FechaMovimiento2 as Fecha_dismi_reserva,VrMovimiento as  Valor_dismin_reserva,-- Reversa 1 Disminuciones 
	null as Fecha_dismi_reserva,null as  Valor_dismin_reserva,-- Reversa 1 Disminuciones 
	FechaMovimiento2 as Fecha_pago_cuota1,VrMovimiento as  cuota1,-- Reversa 2 Pagos
	upper(left(ltrim(rtrim(Nombreasegurado)),50)),'RevPag',id,
	upper(left(ltrim(rtrim(Beneficiariopago)),60)),NumeroIdentificacionBeneficiarioDelPago,Iddoctosoportemanutencion
	 from historicomovimientos (nolock) where  tipoMovimiento  in ('Reversa')
	and llavesiniestro in (select llavesiniestro from historico_inicial where Aval = 0) 
	and fechacontabilizacion is null
	--and year(FechaMovimiento2)=2016 and month(FechaMovimiento2)=8 

	--GENERA LOS XML DE REASEGURO CARDIF RAMO 22
	delete from #reaseg
	insert into #reaseg exec sp_Gen_Xml_Siniestros_ReasegCardif @periodohogar

	insert into #salidaXml(Familia,Periodo,Pasada,Mv,NombreArchivo,Secuencia,Line)
	select Familia,Periodo,2,Mv,null,Secuencia,Line from #reaseg


 ----NO GENERA XML'S SOLO LLENA TABLA QUE NECESITA PARA TRABAJAR
	insert into #asientos exec SiniestrosWp.dbo.sp_asientosSiniestros @ano1,@mes1,4,@nombre


	Update SiniestrosWp.dbo.HistoricoasientosPru set Importe_Transaccion=-Importe_Transaccion,
		Debito_Credito=case Debito_Credito when 'C' then 'D' else 'C' end
	from SiniestrosWp.dbo.HistoricoasientosPru 
------------end 




----GENERA LOS 2 XML FALTANTES PARA REVERSA 
delete from #directas
insert into #directas exec SiniestrosWp.dbo.sp_XMLAsientosPru 'SINIE',@periodo,null,@nombre,'PANTALLA'
insert into #directas exec SiniestrosWp.dbo.sp_XMLAsientosPru 'LRVSI',@periodo,null,@nombre,'PANTALLA'
insert into #directas exec SiniestrosWp.dbo.sp_XMLAsientosPru 'CRVSI',@periodo,null,@nombre,'PANTALLA'

insert into #salidaXml(Familia,Periodo,Pasada,Mv,NombreArchivo,Secuencia,Line)
select 'Directas',@periodohogar,2,Tipo_Diario,NombreArchivo,1,Contenido
from #directas where Contenido is not null



--- Actualiza Registros contabilizados
update historicomovimientos set fechacontabilizacion = dbo.truncdate(getdate()) 
where 
llavesiniestro in (select llavesiniestro from historico_inicial where Aval = 0) 
and fechacontabilizacion is null and marcaavalpos is null



--- Realiza marcación de registros 
delete from controlcierreaval
update historicomovimientos set marcaavalpos = null
where  marcaavalpos is not null

select Familia,Periodo,Pasada,Mv,NombreArchivo,Secuencia,Line
from #salidaXml
order by Pasada,Familia,Mv,Secuencia

END
