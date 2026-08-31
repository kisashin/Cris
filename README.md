--liquibase formatted sql

--changeset j36147:sp_contabiliza_aval_pantalla stripComments:false dbms:mssql
USE [SiniestrosWp]

GO
SET ANSI_NULLS ON
SET QUOTED_IDENTIFIER ON
GO
CREATE OR ALTER PROCEDURE [dbo].[sp_contabiliza_aval](@r int=null)--todo=null,Rev=1, Otros=2
AS
Declare
@fecha varchar(12),
@periodo varchar(12),
@periodohogar varchar(12),
@mes1 int,
@mes2 varchar(2),
@ano1 int,
@ano2 varchar(4),
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

create table #alfa(
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

select @fecha = CONVERT(nvarchar(8),getdate()-5,112)
select @mes2 = substring(@fecha,5,2)
select @ano2 = substring(@fecha,1,5)
select @mes1 = cast(@mes2 as int)
select @ano1 = cast(@ano2 as int)
--select @nombre = case isnull(@r,0) when 1 then 'rv' else '' end +'ASSE' + @fecha + '_ALF'
select @nombre = 'ASSE' + @fecha + '_ALF'
select @periodo = @ano2 + '/0' + @mes2
select @periodohogar = @ano2 + @mes2


---------if @r is null
---------begin
--------	exec sp_contabiliza_aval 2 --Otros mv
--------	exec sp_contabiliza_aval 1 --mv Rever
--------	return 0
---------end
truncate table SiniestrosWp.dbo.tmpsiniestros

-- Aumentos
---if 1<>@r
---begin
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
	tipoMovimiento in('Aumento Reserva','Reserva Inicial - Re-Aseguradora')
	and llavesiniestro in (select llavesiniestro from historico_inicial where Aval = 1) 
	and fechacontabilizacion is null and marcaavalpos is null


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
	upper(left(ltrim(rtrim(Beneficiariopago)),60)),NumeroIdentificacionBeneficiarioDelPago, Iddoctosoportemanutencion
	from historicomovimientos (nolock) where --year(FechaMovimiento2)=2014 and month(FechaMovimiento2)=12 and  
	tipoMovimiento in('Pago')
	and llavesiniestro in (select llavesiniestro from historico_inicial where Aval = 1) 
	and fechacontabilizacion is null and marcaavalpos is null

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
	from historicomovimientos (nolock) where --year(FechaMovimiento2)=2014 and month(FechaMovimiento2)=12 and  
	tipoMovimiento in('Disminución Reserva','Objetado','Anulado ','Anulado','Disminucion Reserva','objecion')
	and llavesiniestro in (select llavesiniestro from historico_inicial where Aval = 1) 
	and fechacontabilizacion is null and marcaavalpos is null

	print @periodohogar
	delete from #alfa
	insert into #alfa exec sp_Gen_Xml_Siniestros_ReasegAlfa @periodohogar

	insert into #salidaXml(Familia,Periodo,Pasada,Mv,NombreArchivo,Secuencia,Line)
	select Familia,Periodo,1,Mv,null,Secuencia,Line from #alfa

	insert into #asientos exec SiniestrosWp.dbo.sp_asientosSiniestros @ano1,@mes1,4,@nombre

	print @periodo
	delete from #directas
	insert into #directas exec SiniestrosWp.dbo.sp_XMLAsientosPru 'SINIE',@periodo,null,@nombre,'PANTALLA'
	insert into #directas exec SiniestrosWp.dbo.sp_XMLAsientosPru 'LRVSI',@periodo,null,@nombre,'PANTALLA'
	insert into #directas exec SiniestrosWp.dbo.sp_XMLAsientosPru 'CRVSI',@periodo,null,@nombre,'PANTALLA'

	insert into #salidaXml(Familia,Periodo,Pasada,Mv,NombreArchivo,Secuencia,Line)
	select 'Directas',@periodohogar,1,Tipo_Diario,NombreArchivo,1,Contenido
	from #directas where Contenido is not null

----end

-----if 1=@r
-----begin
-- Reversa 1  Pagos(Disminuciones)


	select @nombre = 'rvASSE' + @fecha + '_ALF'

	truncate table SiniestrosWp.dbo.tmpsiniestros

	insert into SiniestrosWp.dbo.tmpsiniestros(Numero_radicacion_siniestro,Doc_Asegurado,Cobertura_afectada,cod_producto,cod_plan,Ramo,
	fecha_dismi_reserva,Valor_dismin_reserva,Fecha_pago_cuota1,cuota1,Nombre_asegurado,Poliza,id2,[Nombre_beneficiario ],Resultado_siniestro, Num_planilla)
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
	upper(left(ltrim(rtrim(Beneficiariopago)),60)),NumeroIdentificacionBeneficiarioDelPago, Iddoctosoportemanutencion
	 from historicomovimientos (nolock) where --year(Fechamovimiento2)=2014 and month(Fechamovimiento2)=12 and  
	tipoMovimiento 
	in ('Reversa')
	and llavesiniestro in (select llavesiniestro from historico_inicial where Aval = 1) 
	and fechacontabilizacion is null and marcaavalpos is null
-----end
-- GENERA los archivos XML

--Registra
--Reserva_inicial_constituida='CRVSI'
--Pagos='SINIE'--
--dismi_reserva='LRVSI'--
	
	delete from #alfa
	insert into #alfa exec sp_Gen_Xml_Siniestros_ReasegAlfa @periodohogar

	insert into #salidaXml(Familia,Periodo,Pasada,Mv,NombreArchivo,Secuencia,Line)
	select Familia,Periodo,2,Mv,null,Secuencia,Line from #alfa

	insert into #asientos exec SiniestrosWp.dbo.sp_asientosSiniestros @ano1,@mes1,4,@nombre
------if 1=@r
---begin
--Crea Asiento Reversa= Valor -> -Valor y D->C/C->D
	Update SiniestrosWp.dbo.HistoricoasientosPru set Importe_Transaccion=-Importe_Transaccion,
		Debito_Credito=case Debito_Credito when 'C' then 'D' else 'C' end
	from SiniestrosWp.dbo.HistoricoasientosPru 
----end 

--Genera Xml
--Las reversas tienen el tmpsiniestros.id en GeneralDescription12

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
llavesiniestro in (select llavesiniestro from historico_inicial where Aval = 1) 
and fechacontabilizacion is null and marcaavalpos is null


------- Realiza marcación de registros 

insert into controlcierreaval values (1,getdate())

select Familia,Periodo,Pasada,Mv,NombreArchivo,Secuencia,Line
from #salidaXml
order by Pasada,Familia,Mv,Secuencia

END
