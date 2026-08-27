
GO
SET NOEXEC OFF
GO


--liquibase formatted sql
--changeset j36147:HU_DDPT_566_sp_contabiliza_cardifCentro_20260826_01 splitStatements:true endDelimiter:\nGO stripComments:false dbms:mssql

USE [SiniestrosWp]
GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE OR ALTER PROCEDURE [dbo].[sp_contabiliza_cardifCentro](@r int=null)
AS
Declare
@fecha varchar(12),
@periodo varchar(12),
@periodo2 int;
BEGIN
	SET NOCOUNT ON;

	select @fecha = CONVERT(nvarchar(8),getdate()-7,112);
	select @periodo = substring(@fecha,1,4) + substring(@fecha,5,2);
	select @periodo2 = cast(@periodo as int);

	DROP TABLE IF EXISTS #xmlOut;
	create table #xmlOut(Pasada tinyint null, id int, Mv nvarchar(50), Secuencia bigint, Line nvarchar(max));

	truncate table SiniestrosWp.dbo.TBL_Asientos_siniestro;

	insert into SiniestrosWp.dbo.TBL_Asientos_siniestro(Numero_radicacion_siniestro,Doc_Asegurado,Cobertura_afectada,cod_producto,cod_plan,Ramo,Fecha_aviso_Cardif,Reserva_inicial_constituida,Nombre_asegurado,Poliza,id2,Participacion_Cardif, Moneda)
	Select NumeroSiniestro,
	NroIdentificacion,
	Cobertura,
	CodProducto,
	case when isnumeric(CodPlan)=0 then '0' when isnumeric(CodPlan)>0 and CodPlan > 9 then '0' else isnull(CodPlan,'0') end,
	Ramo,
	FechaMovimiento2,
	vrmovimiento,
	upper(left(ltrim(rtrim(Nombreasegurado)),50)),
	null,
	id_historico_movimiento,
	1,
	Moneda
	from TBL_Historico_Movimientos
	where tipoMovimiento in('Aumento Reserva','Reserva Inicial - Aseguradora')
	and id_historico_movimiento in (select id_historico_movimiento from TBL_historico_inicial)
	and fechacontabilizacion is null;

	insert into SiniestrosWp.dbo.TBL_Asientos_siniestro(Numero_radicacion_siniestro,Doc_Asegurado,Cobertura_afectada,cod_producto,cod_plan,Ramo,
	Fecha_pago_cuota1,cuota1,Nombre_asegurado,Poliza,id2, Participacion_Cardif, Moneda)
	Select NumeroSiniestro,
	NroIdentificacion,
	Cobertura,
	CodProducto,
	case when isnumeric(CodPlan)=0 then '0' when isnumeric(CodPlan)>0 and CodPlan > 9 then '0' else isnull(CodPlan,'0') end,
	Ramo,
	FechaMovimiento2,
	vrmovimiento,upper(left(ltrim(rtrim(Nombreasegurado)),50)),null, id_historico_movimiento, 1, Moneda
	from TBL_Historico_Movimientos where
	tipoMovimiento in('Pago')
	and llavesiniestro in (select llavesiniestro from TBL_historico_inicial)
	and fechacontabilizacion is null;

	insert into SiniestrosWp.dbo.TBL_Asientos_siniestro(Numero_radicacion_siniestro,Doc_Asegurado,Cobertura_afectada,cod_producto,cod_plan,Ramo,
	Fecha_dismi_reserva,Valor_dismin_reserva,Nombre_asegurado,Poliza,id2, Participacion_Cardif, Moneda)
	Select NumeroSiniestro,
	NroIdentificacion,
	Cobertura,
	CodProducto,
	case when isnumeric(CodPlan)=0 then '0' when isnumeric(CodPlan)>0 and CodPlan > 9 then '0' else isnull(CodPlan,'0') end,
	Ramo,
	FechaMovimiento2,
	vrmovimiento,upper(left(ltrim(rtrim(Nombreasegurado)),50)),null, id_historico_movimiento, 1, Moneda
	from TBL_Historico_Movimientos where
	tipoMovimiento in('Disminución Reserva','Objetado','Anulado ','Anulado','Disminucion Reserva','objecion')
	and llavesiniestro in (select llavesiniestro from TBL_historico_inicial)
	and fechacontabilizacion is null;

	insert into #xmlOut(id,Mv,Secuencia,Line)
	exec sp_Gen_Xml_Siniestros_ReasegCentro @periodo2;

	update #xmlOut set Pasada=1 where Pasada is null;

	truncate table SiniestrosWp.dbo.TBL_Asientos_siniestro;

	insert into SiniestrosWp.dbo.TBL_Asientos_siniestro(Numero_radicacion_siniestro,Doc_Asegurado,Cobertura_afectada,cod_producto,cod_plan,Ramo,
	fecha_dismi_reserva,Valor_dismin_reserva,Fecha_pago_cuota1,cuota1,Nombre_asegurado,Poliza,id2,Participacion_Cardif, Moneda)
	Select NumeroSiniestro,
	NroIdentificacion,
	Cobertura,
	CodProducto,
	case when isnumeric(CodPlan)=0 then '0' when isnumeric(CodPlan)>0 and CodPlan > 9 then '0' else isnull(CodPlan,'0') end,
	Ramo,
	null,null,
	FechaMovimiento2,vrmovimiento,
	upper(left(ltrim(rtrim(Nombreasegurado)),50)),'RevPag',id_historico_movimiento, 1, Moneda
	from TBL_Historico_Movimientos where  tipoMovimiento  in ('Reversa')
	and llavesiniestro in (select llavesiniestro from TBL_historico_inicial)
	and fechacontabilizacion is null;

	insert into #xmlOut(id,Mv,Secuencia,Line)
	exec sp_Gen_Xml_Siniestros_ReasegCentro @periodo2;

	update #xmlOut set Pasada=2 where Pasada is null;

	update TBL_Historico_Movimientos
	set fechacontabilizacion = dbo.truncdate(getdate())
	where llavesiniestro in (select llavesiniestro from TBL_historico_inicial)
	and fechacontabilizacion is null;

	select cast(@periodo2 as nvarchar(6)) Periodo, Pasada, id, Mv, Secuencia, Line
	from #xmlOut
	order by Pasada, id, Secuencia;

END;
GO
