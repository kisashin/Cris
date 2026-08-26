--liquibase formatted sql
--changeset j36147:COIMPLUT-35258_Rb_sp_contabiliza_cardifCentro_20260826_01 splitStatements:false

CREATE OR ALTER PROCEDURE [dbo].[sp_contabiliza_cardifCentro](@r int=null)--todo=null,Rev=1, Otros=2
AS
Declare
@fecha varchar(12),
@periodo varchar(12),
@periodo2 int,
@mes1 int,
@mes2 varchar(2),
@ano1 int,
@ano2 varchar(4),
@nombre varchar(40),
@identificador nvarchar(20);
BEGIN

	select @fecha = CONVERT(nvarchar(8),getdate()-7,112);

	select @mes2 = substring(@fecha,5,2);
	select @ano2 = substring(@fecha,1,4);

	select @periodo = @ano2 + @mes2;
	select @periodo2 = cast(@periodo  as int);
	print @periodo2;

	SELECT @identificador = cast(ltrim(str(DATEPART(HH,getdate())))+ltrim(str(DATEPART(MINUTE,getdate())))+ltrim(str(DATEPART(SS,getdate()))) as nvarchar)

	truncate table SiniestrosWp.dbo.TBL_Asientos_siniestro;

	insert
	into
		SiniestrosWp.dbo.TBL_Asientos_siniestro(Numero_radicacion_siniestro,Doc_Asegurado,Cobertura_afectada,cod_producto,cod_plan,Ramo,Fecha_aviso_Cardif,Reserva_inicial_constituida,Nombre_asegurado,Poliza,id2,Participacion_Cardif, Moneda)
	Select
		NumeroSiniestro as Numero_radicacion_siniestro,
		NroIdentificacion as Doc_Asegurado,
		Cobertura as Cobertura_afectada ,
		CodProducto as cod_producto,
		case when isnumeric(CodPlan)=0 then
											'0'
			when isnumeric(CodPlan)>0 and CodPlan > 9 then
											'0'
											else
											isnull(CodPlan,'0')
											end as cod_plan ,
		Ramo,
		FechaMovimiento2 as Fecha_aviso_Cardif,
		vrmovimiento as  Reserva_inicial_constituida,
		upper(left(ltrim(rtrim(Nombreasegurado)),50)),
		null,
		id_historico_movimiento,
		1,
		Moneda
	from TBL_Historico_Movimientos
	where tipoMovimiento in('Aumento Reserva','Reserva Inicial - Aseguradora')
	and id_historico_movimiento in (select
									id_historico_movimiento
							from TBL_historico_inicial
							)
	and fechacontabilizacion is null

	--Pagos

	insert into SiniestrosWp.dbo.TBL_Asientos_siniestro(Numero_radicacion_siniestro,Doc_Asegurado,Cobertura_afectada,cod_producto,cod_plan,Ramo,
	Fecha_pago_cuota1,cuota1,Nombre_asegurado,Poliza,id2, Participacion_Cardif, Moneda)
	Select NumeroSiniestro as Numero_radicacion_siniestro,
	NroIdentificacion as Doc_Asegurado,
	Cobertura as Cobertura_afectada ,
	CodProducto as cod_producto,
	case when isnumeric(CodPlan)=0 then '0' when isnumeric(CodPlan)>0 and CodPlan > 9 then '0' else isnull(CodPlan,'0') end as cod_plan ,
	Ramo,
	FechaMovimiento2 as Fecha_pago_cuota1,
	vrmovimiento as  cuota1,upper(left(ltrim(rtrim(Nombreasegurado)),50)),null, id_historico_movimiento, 1, Moneda
	from TBL_Historico_Movimientos where
	tipoMovimiento in('Pago')
	and llavesiniestro in (select llavesiniestro from TBL_historico_inicial)
	and fechacontabilizacion is null

	--Disminuciones

	insert into SiniestrosWp.dbo.TBL_Asientos_siniestro(Numero_radicacion_siniestro,Doc_Asegurado,Cobertura_afectada,cod_producto,cod_plan,Ramo,
	Fecha_dismi_reserva,Valor_dismin_reserva,Nombre_asegurado,Poliza,id2, Participacion_Cardif, Moneda)
	Select NumeroSiniestro as Numero_radicacion_siniestro,
	NroIdentificacion as Doc_Asegurado,
	Cobertura as Cobertura_afectada ,
	CodProducto as cod_producto,
	case when isnumeric(CodPlan)=0 then '0' when isnumeric(CodPlan)>0 and CodPlan > 9 then '0' else isnull(CodPlan,'0') end as cod_plan ,
	Ramo,
	FechaMovimiento2 as Fecha_dismi_reserva,
	vrmovimiento as  Valor_dismin_reserva,upper(left(ltrim(rtrim(Nombreasegurado)),50)),null, id_historico_movimiento, 1, Moneda
	from TBL_Historico_Movimientos where
	tipoMovimiento in('Disminución Reserva','Objetado','Anulado ','Anulado','Disminucion Reserva','objecion')
	and llavesiniestro in (select llavesiniestro from TBL_historico_inicial)
	and fechacontabilizacion is null

	--GENERA XML
	exec sp_Gen_Xml_Siniestros_ReasegCentro @periodo2;

	-- Reversa

	truncate table SiniestrosWp.dbo.TBL_Asientos_siniestro;

	insert into SiniestrosWp.dbo.TBL_Asientos_siniestro(Numero_radicacion_siniestro,Doc_Asegurado,Cobertura_afectada,cod_producto,cod_plan,Ramo,
	fecha_dismi_reserva,Valor_dismin_reserva,Fecha_pago_cuota1,cuota1,Nombre_asegurado,Poliza,id2,Participacion_Cardif, Moneda)
	Select NumeroSiniestro as Numero_radicacion_siniestro,
	NroIdentificacion as Doc_Asegurado,
	Cobertura as Cobertura_afectada ,
	CodProducto as cod_producto,
	case when isnumeric(CodPlan)=0 then '0' when isnumeric(CodPlan)>0 and CodPlan > 9 then '0' else isnull(CodPlan,'0') end as cod_plan ,
	Ramo,
	null as Fecha_dismi_reserva,null as  Valor_dismin_reserva,-- Reversa 1 Disminuciones
	FechaMovimiento2 as Fecha_pago_cuota1,vrmovimiento as  cuota1,-- Reversa 2 Pagos
	upper(left(ltrim(rtrim(Nombreasegurado)),50)),'RevPag',id_historico_movimiento, 1, Moneda
	from TBL_Historico_Movimientos where 	tipoMovimiento 	in ('Reversa')
	and llavesiniestro in (select llavesiniestro from TBL_historico_inicial)
	and fechacontabilizacion is null

	--GENERA XML
	exec sp_Gen_Xml_Siniestros_ReasegCentro @periodo2;


	update
		TBL_Historico_Movimientos
	set fechacontabilizacion = dbo.truncdate(getdate())
	where llavesiniestro in (
							 select
								llavesiniestro
							 from TBL_historico_inicial)
	and fechacontabilizacion is null

END
