USE [SiniestrosWp]
GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

ALTER   PROCEDURE [dbo].[sp_contabiliza_coaseguro]
AS
Declare
@fecha varchar(12),
@periodo varchar(12),
@periodo2 int,
@mes1 int,
@mes2 varchar(2),
@ano1 int,
@ano2 varchar(4),
@nombre varchar(40);

BEGIN
SET NOCOUNT ON;

create table #coaseguro(
	Familia varchar(50),
	Periodo nvarchar(6),
	Mv varchar(50),
	Secuencia bigint,
	Line nvarchar(max));

select @fecha = CONVERT(nvarchar(8),getdate()-5,112);

select @mes2 = substring(@fecha,5,2);
select @ano2 = substring(@fecha,1,4);


select @periodo = @ano2 + @mes2;
select @periodo2 = cast(@periodo  as int);

delete from SiniestrosWp.dbo.tmpsiniestros;

	-- Aumentos


	insert into SiniestrosWp.dbo.tmpsiniestros(Numero_radicacion_siniestro,Doc_Asegurado,
	Cobertura_afectada,cod_producto,cod_plan,Ramo,Fecha_aviso_Cardif,Reserva_inicial_constituida,Nombre_asegurado,Poliza,id2,Participacion_Cardif)
	Select NumeroSiniestro as Numero_radicacion_siniestro,
	NroIdentificacion as Doc_Asegurado,
	Cobertura as Cobertura_afectada ,
	CodProducto as cod_producto,
	case when isnumeric(CodPlan)=0 then '0' when isnumeric(CodPlan)>0 and CodPlan > 9 then '0' else isnull(CodPlan,'0') end as cod_plan ,
	Ramo,
	FechaMovimiento2 as Fecha_aviso_Cardif,
	VrMovimiento as  Reserva_inicial_constituida,upper(left(ltrim(rtrim(Nombreasegurado)),50)),null, id, round(vrcoaseguroretenido/Vrmovimiento,1)
	from historicomovimientos (nolock) where
	tipoMovimiento in('Aumento Reserva','Reserva Inicial - Aseguradora')
	and llavesiniestro in (select llavesiniestro from historico_inicial where Aval = 0) 
	and fechacontabilizacion is null and tipocoaseguro is not null
	;


	--Pagos

	insert into SiniestrosWp.dbo.tmpsiniestros(Numero_radicacion_siniestro,Doc_Asegurado,Cobertura_afectada,cod_producto,cod_plan,Ramo,
	Fecha_pago_cuota1,cuota1,Nombre_asegurado,Poliza,id2,Participacion_Cardif)
	Select NumeroSiniestro as Numero_radicacion_siniestro,
	NroIdentificacion as Doc_Asegurado,
	Cobertura as Cobertura_afectada ,
	CodProducto as cod_producto,
	case when isnumeric(CodPlan)=0 then '0' when isnumeric(CodPlan)>0 and CodPlan > 9 then '0' else isnull(CodPlan,'0') end as cod_plan ,
	Ramo,
	FechaMovimiento2 as Fecha_pago_cuota1,
	VrMovimiento as  cuota1,upper(left(ltrim(rtrim(Nombreasegurado)),50)),null, id, round(vrcoaseguroretenido/Vrmovimiento,1)
	from historicomovimientos (nolock) where 
	tipoMovimiento in('Pago')
	and llavesiniestro in (select llavesiniestro from historico_inicial where Aval = 0) 
	and fechacontabilizacion is null and tipocoaseguro is not null
	;

	--Disminuciones

	insert into SiniestrosWp.dbo.tmpsiniestros(Numero_radicacion_siniestro,Doc_Asegurado,Cobertura_afectada,cod_producto,cod_plan,Ramo,
	Fecha_dismi_reserva,Valor_dismin_reserva,Nombre_asegurado,Poliza,id2,Participacion_Cardif)
	Select NumeroSiniestro as Numero_radicacion_siniestro,
	NroIdentificacion as Doc_Asegurado,
	Cobertura as Cobertura_afectada ,
	CodProducto as cod_producto,
	case when isnumeric(CodPlan)=0 then '0' when isnumeric(CodPlan)>0 and CodPlan > 9 then '0' else isnull(CodPlan,'0') end as cod_plan ,
	Ramo,
	FechaMovimiento2 as Fecha_dismi_reserva,
	VrMovimiento as  Valor_dismin_reserva,upper(left(ltrim(rtrim(Nombreasegurado)),50)),null, id, round(vrcoaseguroretenido/Vrmovimiento,1)
	from historicomovimientos (nolock) where 
	tipoMovimiento in('Disminución Reserva','Objetado','Anulado ','Anulado','Disminucion Reserva','objecion')
	and llavesiniestro in (select llavesiniestro from historico_inicial where Aval = 0) 
	and fechacontabilizacion is null and tipocoaseguro is not null
	;


	insert into SiniestrosWp.dbo.tmpsiniestros(Numero_radicacion_siniestro,Doc_Asegurado,Cobertura_afectada,cod_producto,cod_plan,Ramo,
	fecha_dismi_reserva,Valor_dismin_reserva,Fecha_pago_cuota1,cuota1,Nombre_asegurado,Poliza,id2,Participacion_Cardif)
	Select NumeroSiniestro as Numero_radicacion_siniestro,
	NroIdentificacion as Doc_Asegurado,
	Cobertura as Cobertura_afectada ,
	CodProducto as cod_producto,
	case when isnumeric(CodPlan)=0 then '0' when isnumeric(CodPlan)>0 and CodPlan > 9 then '0' else isnull(CodPlan,'0') end as cod_plan ,
	Ramo,
	null as Fecha_dismi_reserva,null as  Valor_dismin_reserva,-- Reversa 1 Disminuciones 
	FechaMovimiento2 as Fecha_pago_cuota1,VrMovimiento as  cuota1,-- Reversa 2 Pagos
	upper(left(ltrim(rtrim(Nombreasegurado)),50)),'RevPag',id, round(vrcoaseguroretenido/Vrmovimiento,1)
	 from historicomovimientos (nolock) where 	tipoMovimiento 	in ('Reversa')
	and llavesiniestro in (select llavesiniestro from historico_inicial where Aval = 0) 
	and fechacontabilizacion is null and tipocoaseguro is not null
	;

--GENERA XML

insert into #coaseguro exec sp_Gen_Xml_Siniestros_CoaseguroC @periodo2;
 

--- Actualiza Registros contabilizados


update historicomovimientos set fechacontabilizacion = dbo.truncdate(getdate()) 
where 
llavesiniestro in (select llavesiniestro from historico_inicial where Aval = 0) 
and fechacontabilizacion is null and marcaavalpos is null and tipocoaseguro is not null 
--and year(FechaMovimiento2)=2016 and month(FechaMovimiento2)=8 
;

select Familia,Periodo,Mv,Secuencia,Line
from #coaseguro
order by Familia,Mv,Secuencia;



END
GO
