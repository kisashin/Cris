--liquibase formatted sql
--changeset j36147:HU_Reaseguro_566_sp_XMLAsientosPru_20260903_01 stripComments:false dbms:mssql

USE [CardifWP]

GO
SET ANSI_NULLS ON
SET QUOTED_IDENTIFIER ON
GO

--exec dbo.sp_XMLAsientosPru 'SINIE','2011/004',null,'V3'
--exec dbo.sp_XMLAsientosPru 'ANUDI','2011/004','0909','ANU FEB' 
--exec dbo.sp_XMLAsientosPru 'EMIDI','2011/005','0101'
--exec dbo.sp_XMLAsientosPru 'REVAR','2013/011','0000','REVER_201310',''
CREATE OR ALTER PROCEDURE  [dbo].[sp_XMLAsientosPru](@Tipo_Diario varchar(50)=null,@Periodo_Contable varchar(10)=null,@Producto Varchar(10)=null,@ajuste varchar(100)=null,@XmlDestino  varchar(10)='SUN'  )
as
BEGIN
SET NOCOUNT ON;
declare @cmd nvarchar(max),@ar nvarchar(100),@Prod Varchar(10);
set @Prod=isnull(@Producto,'')
set @Prod=case when left(@Prod,1)='0' then substring(@Prod,2,4) else @Prod end;
set @ar=rtrim(ltrim(left(isnull(@ajuste,''),20)))+@Tipo_Diario+'_'
set @ar=@ar+@Prod+replace(@Periodo_Contable,'/0','')+'.XML';
set @ar=replace(@ar,' ','_');
if len(ltrim(rtrim(@Producto)))<4 set @Producto='0'+ltrim(rtrim(@Producto));
update HistoricoAsientosPru set [IdPlan]='99999'
where IdPlan is null or IdPlan='' or IdPlan='0' 
and (Periodo_Contable=@Periodo_Contable)

update HistoricoAsientosPru set [Ramo]=(select ramo from producto where 
	cast(HistoricoAsientosPru.[Producto]as int)=producto.id)
where [Ramo]='' or [Ramo] is null --and tipo_diario='ANUDI'
and (Periodo_Contable=@Periodo_Contable)

update HistoricoAsientosPru set [Producto]='0405'
where [Producto]='405'--and tipo_diario='ANUDI'
and (Periodo_Contable=@Periodo_Contable )

update HistoricoAsientosPru set IdPlan='99999'
where producto in (3501,3502,3503,3504,3505,3506)
and Periodo_Contable=@Periodo_Contable  and IdPlan<>'99999'

update HistoricoAsientosPru set [Producto] ='1003'
where [Producto]='01003'
and (Periodo_Contable=@Periodo_Contable )

update HistoricoAsientosPru set [Producto] ='1401'
where [Producto]='01401'
and (Periodo_Contable=@Periodo_Contable )

update HistoricoAsientosPru set [Producto] ='1402'
where [Producto]='01402'
and (Periodo_Contable=@Periodo_Contable )

update HistoricoAsientosPru set [Producto] ='1901'
where [Producto]='01901'
and (Periodo_Contable=@Periodo_Contable )

update HistoricoAsientosPru set [Producto] ='1904'
where [Producto]='01904'
and (Periodo_Contable=@Periodo_Contable )
update HistoricoAsientosPru set [Producto] ='0301'
where [Producto]='301'
and (Periodo_Contable=@Periodo_Contable )

update HistoricoAsientosPru set [Ramo] =right('00'+right(ramo,1),2)--'09'
where len(ltrim(rtrim(ramo)))<2--[Ramo]='9'  
and (Periodo_Contable=@Periodo_Contable )

update HistoricoAsientosPru set [NIT_Cedula] ='366964'
where [NIT_Cedula]='E366964'
and (Periodo_Contable=@Periodo_Contable );

update HistoricoAsientosPru set Cobertura='99999' where tipo_diario in('SINIE','LRVSI','CRVSI');


--delete from dbo.##sp_HistoricoAsientos  where cobertura='INC. TEMPORAL'
update HistoricoAsientosPru set cobertura='INCAP.TOT.TEMP.'
where cobertura='INCAPACIDAD TOTAL TE'
and (Periodo_Contable=@Periodo_Contable )

update HistoricoAsientosPru set cobertura='INCAP.TOT.TEMP.'
where cobertura='INCAP TOTAL TEMPORAL'
and (Periodo_Contable=@Periodo_Contable )

update HistoricoAsientosPru set cobertura='MUERTE ACCIDENT'
where cobertura='MUERTE ACCIDENTAL'
and (Periodo_Contable=@Periodo_Contable )

update HistoricoAsientosPru set cobertura='ENFEMEDADGRAVE'
where cobertura='ENFERMEDADES GRAVES'
and (Periodo_Contable=@Periodo_Contable )

update HistoricoAsientosPru set Cobertura='ENFEMEDADGRAVE'
where Cobertura='ENFERMEDA.GRAVE'--and tipo_diario='RVARC'
and (Periodo_Contable=@Periodo_Contable )

update HistoricoAsientosPru set Cobertura='ENFEMEDADGRAVE'
where Cobertura='ENFERMEDADGRAVE'--and tipo_diario='RVARC'
and (Periodo_Contable=@Periodo_Contable )

update HistoricoAsientosPru set Cobertura='INCAP.TOT.TEMP.'
where Cobertura='INCA.TOT.TEMP.'--and tipo_diario='RVARC'
and (Periodo_Contable=@Periodo_Contable )

update HistoricoAsientosPru set [Descripcion]=replace([Descripcion],'?','N')
where Periodo_Contable=@Periodo_Contable

update HistoricoAsientosPru set [Descripcion]=replace([Descripcion],'"','')
where Periodo_Contable=@Periodo_Contable


update HistoricoAsientosPru set cobertura='DAÑOACCMERCANCI' where cobertura='DA&#209;OACCMERCANCI'
update HistoricoAsientosPru set cobertura='DAÑOACCMERCANCI' where cobertura='DA¥OACCMERCANCI'
update HistoricoAsientosPru set cobertura='DAÑOACCMERCANCI' where cobertura='DA?OACCMERCANCI'
update HistoricoAsientosPru set cobertura='DAÑO ACCIDENTAL' where cobertura='DA&#209;O ACCIDENTAL'
update HistoricoAsientosPru set cobertura='DAÑOMERCANCIA' where cobertura='DA&#209;OMERCANCIA'
update HistoricoAsientosPru set cobertura='DAÑO ACCIDENTAL' where cobertura='DA?O ACCIDENTAL'
update HistoricoAsientosPru set cobertura='GARANTÍA EXTEN.' where cobertura='GARANT&#205;A EXTEN.'
update HistoricoAsientosPru set cobertura='GARANTÍA EXTEN.' where cobertura='GARANTIA EXTENDIDA'

update HistoricoAsientosPru set descripcion='COMPAÑIA DE FINANCIAMIENTO TUYA S.A.' where descripcion='COMPA&amp;#209;IA DE FINANCIAMIENTO TUYA S.A.'
update HistoricoAsientosPru set descripcion='COMPAÑIA DE FINANCIAMIENTO TUYA S.A.' where descripcion='COMPA&#209;IA DE FINANCIAMIENTO TUYA S.A.'
update HistoricoAsientosPru set descripcion='JARDINE LLOYD THOMPSON VALENCIA Y IRAGORRI COREDORES DE SEGUROS S.A.' where descripcion='JARDINE LLOYD THOMPSON VALENCIA &amp; IRAGORRI COREDORES DE SEGUROS S.A.'

	--LITCOSOP-3284
	update HistoricoAsientosPru set Debito_Credito='C', Importe_Transaccion = -abs(Importe_Transaccion)  where Periodo_Contable=@Periodo_Contable 
	--and  codigo_cuenta='51021000' 
	and (cast(producto as int) in(601,609)) and ramo in(31,34)  
	and tipo_diario='SINIE'
	and Debito_Credito='D'
	and codigo_cuenta='51144000';
	
update HistoricoAsientosPru set debito_credito='D' where tipo_diario='RVARC'
and debito_credito='C'and importe_transaccion>0
and (Tipo_Diario=@Tipo_Diario and Periodo_Contable=@Periodo_Contable and   (@Producto='0000' or Producto=@Producto)  and  Descripcion_Asiento=@ajuste)

update HistoricoAsientosPru set debito_credito='C' where tipo_diario='RVARC'
and debito_credito='D'and importe_transaccion<0  
and (Periodo_Contable=@Periodo_Contable )

update HistoricoAsientosPru set [Importe_Transaccion]=cast([Importe_Transaccion]as decimal(20,0)) 
where  (Tipo_Diario=@Tipo_Diario and Periodo_Contable=@Periodo_Contable and  (@Producto='0000' or Producto=@Producto)  and  Descripcion_Asiento=@ajuste)

delete from HistoricoAsientosPru where Importe_transaccion=0 or Importe_transaccion is null or Importe_transaccion=''

update HistoricoAsientosPru set Origen_Diario='SSC' where Origen_Diario='LVT' and Periodo_Contable=@Periodo_Contable
update HistoricoAsientosPru  set NoSiniestro='' where NoSiniestro is null;
-----------------------
	--COSD-8352: Cambiar 19154001 por 19209503
update HistoricoAsientosPru set codigo_cuenta='19209503' 
	where Periodo_Contable=@Periodo_Contable  and codigo_cuenta='19154001'; 

update HistoricoAsientosPru set codigo_cuenta='51958500' -- Con CONTRATO DE USO DE RED (COMIS_PAG_SOC+DISMI_ANOACT_COM_SOC+LIB_ANOANT_COM_SOC)
	where tipo_diario='RVARC' and Periodo_Contable=@Periodo_Contable
		and codigo_cuenta='51959500' 
		and (cast(producto as int) in(430) OR CAST(socio AS INT) in(1,8,14,16,18,19,33,25,35,4,56,58,59,63,64,9));
																	

------------------
------------------
--Nuevas Cuentas producto de Grantia Extendida COSD-10685
if exists(select 1 from HistoricoAsientosPru where Periodo_Contable=@Periodo_Contable and (cast(producto as int) in(152,151,150,4101 , 2902) and tipo_diario in('SINIE','LRVSI','CRVSI')))
begin
	update HistoricoAsientosPru set codigo_cuenta='15600505'   where Periodo_Contable=@Periodo_Contable and  codigo_cuenta='15600501' and (cast(producto as int) in(152,151,150,4101 , 2902));
	update HistoricoAsientosPru set codigo_cuenta='15600506'   where Periodo_Contable=@Periodo_Contable and  codigo_cuenta='15600502' and (cast(producto as int) in(152,151,150,4101 , 2902));
	update HistoricoAsientosPru set codigo_cuenta='28810503'   where Periodo_Contable=@Periodo_Contable and  codigo_cuenta='28810500' and (cast(producto as int) in(152,151,150,4101 , 2902));
	update HistoricoAsientosPru set codigo_cuenta='28959553'   where Periodo_Contable=@Periodo_Contable and  codigo_cuenta='28959500' and (cast(producto as int) in(152,151,150,4101 , 2902));
	update HistoricoAsientosPru set codigo_cuenta='41020502'   where Periodo_Contable=@Periodo_Contable and  codigo_cuenta='41020500' and (cast(producto as int) in(152,151,150,4101 , 2902));
	update HistoricoAsientosPru set codigo_cuenta='41027503'   where Periodo_Contable=@Periodo_Contable and  codigo_cuenta='41027500' and (cast(producto as int) in(152,151,150,4101 , 2902));
	if exists(select 1 from HistoricoAsientosPru where Periodo_Contable=@Periodo_Contable and (cast(producto as int) in(150,151,152,4101 , 2902) and tipo_diario in('LRVSI','CRVSI')))
	begin
		update HistoricoAsientosPru set codigo_cuenta='26540503'   
		where Periodo_Contable=@Periodo_Contable 
			and  codigo_cuenta='26540501' 
			and (cast(producto as int) in(152,151,150,4101 , 2902))  
			and tipo_diario='CRVSI';
		
		update HistoricoAsientosPru set codigo_cuenta='51110504'   
		where Periodo_Contable=@Periodo_Contable 
			and codigo_cuenta='51110501' 
			and (cast(producto as int) in(152,151,150,4101 , 2902))  
			and tipo_diario='CRVSI';
		
		--LITCOSOP-3284
		update HistoricoAsientosPru set Debito_Credito='C', Importe_Transaccion = -abs(Importe_Transaccion)  
		where Periodo_Contable=@Periodo_Contable 
		--and  codigo_cuenta='51021000' 
			and (cast(producto as int) in(601,609)) and ramo in(31,34)  
			and tipo_diario='SINIE'
			and Debito_Credito='D'
			and codigo_cuenta='51144000';
			
		update HistoricoAsientosPru set codigo_cuenta='26540503'   
		where Periodo_Contable=@Periodo_Contable 
			and  codigo_cuenta='26540501' 
			and (cast(producto as int) in(152,151,150,4101 , 2902))  
			and tipo_diario='LRVSI';
		
		update HistoricoAsientosPru set codigo_cuenta='41110503'   
		where Periodo_Contable=@Periodo_Contable 
			and  codigo_cuenta='41110501' 
			and (cast(producto as int) in(152,151,150,4101 , 2902))  
			and tipo_diario='LRVSI';
	
	end;
end;
------------------
begin try drop table  #sp_HistoricoAsientosPru; end try begin catch end catch;
select Tipo_Diario,Periodo_Contable,Fecha_Transaccion,Codigo_Cuenta,Ref_Transaccion,Descripcion,Fecha_Vencimiento,Codigo_Moneda,sum(Importe_Transaccion)Importe_Transaccion,
Importe_Base,Debito_Credito,Centro_Costos,Producto,Ramo,Impuestos,Socio,Nit_Cedula,Clave_Asesor,'99999'Cobertura,X_Definir,IdPlan,Origen_Diario,Formato,Fecha_Proceso,Descripcion_Asiento,Estado,NoSiniestro
  into #sp_HistoricoAsientosPru  from dbo.HistoricoAsientosPru 
  where  Tipo_Diario=@Tipo_Diario and Periodo_Contable=@Periodo_Contable and round(Importe_Transaccion,0)<>0 
  and ( (@Producto='0000' or Producto=@Producto)  or @producto is null) and  (Descripcion_Asiento=@ajuste or @ajuste is null)
group by Tipo_Diario,Periodo_Contable,Fecha_Transaccion,Codigo_Cuenta,Ref_Transaccion,Descripcion,Fecha_Vencimiento,Codigo_Moneda,
Importe_Base,Debito_Credito,Centro_Costos,Producto,Ramo,Impuestos,Socio,Nit_Cedula,Clave_Asesor,X_Definir,IdPlan,Origen_Diario,Formato,Fecha_Proceso,Descripcion_Asiento,Estado,NoSiniestro;

delete #sp_HistoricoAsientosPru   where  Codigo_Cuenta is null;
update #sp_HistoricoAsientosPru set [Ref_Transaccion]=replace(replace(replace(replace(left([Ref_Transaccion],29),'é','e'),'ó','o'),'í','i'),'ñ','n'),
Descripcion=replace(replace(replace(replace(replace(replace(replace(left([Descripcion],49),'é','e'),'ó','o'),'í','i'),'ñ','n'),'Ñ','N'),'Á','A'),'Ó','O');

update #sp_HistoricoAsientosPru set Cobertura='99999' where tipo_diario in('SINIE','LRVSI','CRVSI') and Cobertura<>'99999' ;
update #sp_HistoricoAsientosPru set Codigo_Cuenta='23550000' where  tipo_diario in('SINIE','LRVSI','CRVSI') 
														 and producto in(select distinct producto from cardifWp.dbo.prp(nolock) where grupo='C' and socio not in(21,29,41))
														 and Codigo_Cuenta='15082001' and Debito_Credito='C';
update #sp_HistoricoAsientosPru set Codigo_Cuenta='51020500' where  tipo_diario in('SINIE','LRVSI','CRVSI') and ramo in('09','24')
														 and producto in(select distinct producto from cardifWp.dbo.prp(nolock) where grupo='C' and socio not in(21,29,41))
														 and Codigo_Cuenta='51144000' and Debito_Credito='D';
update #sp_HistoricoAsientosPru set Codigo_Cuenta='51021000' where  tipo_diario in('SINIE','LRVSI','CRVSI') and ramo in('31','34')
														 and producto in(select distinct producto from cardifWp.dbo.prp(nolock) where grupo='C' and socio not in(21,29,41))
														 and Codigo_Cuenta='51144000' and Debito_Credito='D';
														 
update #sp_HistoricoAsientosPru set Codigo_Cuenta='23550000' where  tipo_diario in('SINIE','LRVSI','CRVSI') 
														 and producto in(select distinct producto from cardifWp.dbo.prp(nolock) where grupo='C' and socio not in(21,29,41))
														 and Codigo_Cuenta='15082001' and Debito_Credito='D';
update #sp_HistoricoAsientosPru set Codigo_Cuenta='51020500' where  tipo_diario in('SINIE','LRVSI','CRVSI') and ramo in('09','24')
														 and producto in(select distinct producto from cardifWp.dbo.prp(nolock) where grupo='C' and socio not in(21,29,41))
														 and Codigo_Cuenta='51144000' and Debito_Credito='C';
update #sp_HistoricoAsientosPru set Codigo_Cuenta='51021000' where  tipo_diario in('SINIE','LRVSI','CRVSI') and ramo in('31','34')
														 and producto in(select distinct producto from cardifWp.dbo.prp(nolock) where grupo='C' and socio not in(21,29,41))
														 and Codigo_Cuenta='51144000' and Debito_Credito='C';



/*
Select *  into ##sp_HistoricoAsientosPru from dbo.HistoricoAsientosPru
  where  Tipo_Diario=@Tipo_Diario and Periodo_Contable=@Periodo_Contable 
  and ( (@Producto='0000' or Producto=@Producto)  or @producto is null) and  (Descripcion_Asiento=@ajuste or @ajuste is null)
   and round(Importe_Transaccion,0)<>0*/
update #sp_HistoricoAsientosPru set NoSiniestro='' where ascii(NoSiniestro)=160;   
--select * from   ##sp_HistoricoAsientosPru 
declare @varxml as varchar(max)
set @varxml = null
set @varxml=(
select top 1
	(select top 1 'S01'as BusinessUnit,'A'as BudgetCode 
	 from #sp_HistoricoAsientosPru as SunSystemsContext FOR XML AUTO,TYPE, ELEMENTS),
		(select  top 1 	
			(select[Tipo_Diario]as JournalType,(substring([Periodo_Contable],6,8)+substring([Periodo_Contable],1,4))as AccountingPeriod,
				replace(case substring([Fecha_Transaccion],5,1)when '/'then (substring([Fecha_Transaccion],9,2)+'/'+substring([Fecha_Transaccion],6,2)+'/'+substring([Fecha_Transaccion],1,4))
					else [Fecha_Transaccion]end
				,'/','')as TransactionDate,
				[Codigo_Cuenta]as AccountCode,[Ref_Transaccion] as TransactionReference,
				replace(case substring([Fecha_Transaccion],5,1)when '/'then (substring([Fecha_Transaccion],9,2)+'/'+substring([Fecha_Transaccion],6,2)+'/'+substring([Fecha_Transaccion],1,4))
					else [Fecha_Transaccion]end
				,'/','')as ValuDate,				[Descripcion] as Description,
				case substring([Fecha_Vencimiento],5,1)when '/' then (substring([Fecha_Vencimiento],1,2)+'0'+substring([Fecha_Vencimiento],4,1)+substring([Fecha_Vencimiento],6,9))
				else replace([Fecha_Vencimiento],'/','') end as DueDate,[Codigo_Moneda]as CurrencyCode,cast([Importe_Transaccion]as decimal(20,0))as TransactionAmount,
				'2' as TransactionAmountDecimalPlaces,
				'' as BaseAmount,
				'*'as BaseOperator ,
				1 as BaseRate,
				1 as ConversionRate,
				[Debito_Credito]as DebitCredit,[Centro_Costos]as AnalysisCode1,[Producto]as AnalysisCode2,[Ramo]as AnalysisCode3,
				[Impuestos]as AnalysisCode4,[Socio]as AnalysisCode5,[NIT_Cedula]as AnalysisCode6,[Clave_Asesor]as AnalysisCode7,
				[Cobertura]as AnalysisCode8,
				'' as AnalysisCode9 ,case [IdPlan]when ''then '99999' else '99999' end as AnalysisCode10,
				(select top 1  NoSiniestro as GeneralDescription1,  
					''as GeneralDescription2,					''as GeneralDescription3,
					''as GeneralDescription4,
					''as GeneralDescription5,
					''as GeneralDescription6,
					''as GeneralDescription7,
					''as GeneralDescription8,
					''as GeneralDescription9,
					''as GeneralDescription10,
					''as GeneralDescription11,
					case when isnull(x_Definir,'0')='0' then '' else x_Definir end as GeneralDescription12,-->id Reversa
					isnull(left(@ar,30),'') as GeneralDescription13 --Nombre Xml
				from #sp_HistoricoAsientosPru as DetailLad 
						where /*((@Tipo_Diario is null) or (Tipo_Diario=@Tipo_Diario)) and ((@Producto is null) or ( (@Producto='0000' or Producto=@Producto) ))
						 and ((@Periodo_Contable is null) or (Periodo_Contable=@Periodo_Contable))
						 and ((@ajuste is null) or (Descripcion_Asiento=@ajuste))
						and estado='Pendiente XML' 
						and round(Importe_Transaccion,0)<>0 and */
						DetailLad.NoSiniestro=Line.NoSiniestro  --Validacion para el campo NoSiniestro 24/01/2012
						FOR XML AUTO,TYPE, ELEMENTS ),						
					[Origen_Diario]as JournalSource
			from #sp_HistoricoAsientosPru as Line 
/*					where ((@Tipo_Diario is null) or (Tipo_Diario=@Tipo_Diario)) and ((@Producto is null) or ( (@Producto='0000' or Producto=@Producto) ))
						 and ((@Periodo_Contable is null) or (Periodo_Contable=@Periodo_Contable))
						 and ((@ajuste is null) or (Descripcion_Asiento=@ajuste))
						and estado='Pendiente XML' and round(Importe_Transaccion,0)<>0*/
				FOR XML AUTO, ROOT ('Ledger'),Type, ELEMENTS)
	   from #sp_HistoricoAsientosPru as Payload 
/*			where  ((@Tipo_Diario is null) or (Tipo_Diario=@Tipo_Diario)) and ((@Producto is null) or ( (@Producto='0000' or Producto=@Producto) ))
						 and ((@Periodo_Contable is null) or (Periodo_Contable=@Periodo_Contable)) 
						 and ((@ajuste is null) or (Descripcion_Asiento=@ajuste))
					     and estado='Pendiente XML' and round(Importe_Transaccion,0)<>0
*/					     
			FOR XML AUTO,TYPE, ELEMENTS	)
from #sp_HistoricoAsientosPru 
/*	where ((@Tipo_Diario is null) or (Tipo_Diario=@Tipo_Diario)) and ((@Producto is null) or ( (@Producto='0000' or Producto=@Producto) ))
						 and ((@Periodo_Contable is null) or (Periodo_Contable=@Periodo_Contable)) 
						 and ((@ajuste is null) or (Descripcion_Asiento=@ajuste))
						 and estado='Pendiente XML' and round(Importe_Transaccion,0)<>0
*/
		FOR XML PATH('SSC') 

)
--exec dbo.sp_XMLAsientosPru 'EMIDI','2013/007','3802','Emidi  201304 en 201307'
print('entra 1')
if @varxml is not null and @XmlDestino <> 'PANTALLA' select '<?xml version="1.0" encoding="UTF-8" ?>'+ @varxml as dataXml;


if (select count(*) from PatronxProd_siniestros where producto=@Prod )>=0 or @Tipo_Diario='RVARC'   ---Siniestros reaseguro puro ----@Prod si es nulo ya viene como ''

Begin
	if @varxml is not null and @XmlDestino <> 'PANTALLA'
	begin
		IF OBJECT_ID ('dbo._##XML_Asiento','U') IS NOT NULL
		begin
			truncate table dbo._##XML_Asiento;
			insert into dbo._##XML_Asiento select '<?xml version="1.0" encoding="UTF-8" ?>'+ @varxml as dataXml;
		end
		else
		begin
			select '<?xml version="1.0" encoding="UTF-8" ?>'+ @varxml as dataXml into dbo._##XML_Asiento;
		end
		--Escribe XML	
		--declare @cmd nvarchar(1000), @ar nvarchar(1000)='pru.xml'
		--set @cmd=char(39)+'bcp "select dataXml from cardifwp.dbo._##XML_Asiento" queryout \\'+replace(@@SERVERNAME,'\CARDIFWP','')+'\Carguesocios\Salida\XML\'+@ar+' -T -CRAW -c -S'+@@SERVERNAME+char(39)+',no_output';
		
		set @cmd=char(39)+'bcp "select dataXml from cardifwp.dbo._##XML_Asiento"  queryout "d:\Carguesocios\Salida\XML\'+@ar+'" -dSiniestrosWp -T  -S '+@@SERVERNAME+' -T -c -dSiniestrosWp -CRAW'', no_output';

		set @cmd='EXEC master..xp_cmdshell '+@cmd
		--print @cmd

		
		--exec(@cmd)
		--Migracion NEOS 2015/09/11
exec NEOS_BCP_exec @cmd;
		print @cmd
		--Copia para SUN
		/**COAASDK-21792**/
		exec xp_cmdshell 'net use x: "\\amcobgfp01wp\Soluciones"  /persistent:yes';
		--exec xp_cmdshell 'dir /s t:\'
		set @cmd='exec xp_cmdshell "copy \\amcobgfp01wp\Carguesocios\Salida\XML\'+@ar + ' x:\T_CONTABILIDAD\XML_RESERVA"' ;
		set @cmd=replace(@cmd,'"',char(39));
		exec (@cmd);
				--drop table dbo._##XML_Asiento
	end;
end;

if @XmlDestino = 'PANTALLA'
begin
	select @Tipo_Diario Tipo_Diario,
	       @ar NombreArchivo,
	       case when @varxml is null then null
	            else '<?xml version="1.0" encoding="UTF-8" ?>' + @varxml
	       end Contenido;
	return 0;
end;

--if @varxml is not null select '<?xml version="1.0" encoding="UTF-8" ?>'+ @varxml as dataXml;
if @varxml is  null select '0';  
--print len('<?xml version="1.0" encoding="UTF-8" ?>'+ @varxml)
-->>update ha set estado='Pendiente XML' where periodo_contable='2013/008' and producto='0105' and tipo_diario='EMIDI' and  descripcion_asiento is null
-->>select distinct descripcion_asiento,estado from ha where periodo_contable='2013/008' and producto='0105' and tipo_diario='EMIDI';
-->>exec dbo.sp_XMLAsientosPru 'EMIDI','2013/008','0105',null,'TEST' 
--exec dbo.sp_AsientosxSocio_NewXML 2013,8,105,-1,'3',null,null,6,'EMIDI' 
--select top 20 * from HistoricoAsientosPru
/*
if dbo.fExisteTmp('##tmpXml')>0  drop table  ##tmpXml;
select '<?xml version="1.0" encoding="UTF-8" ?>'+ @varxml as dataXml into ##tmpXml;
select * from ##tmpXml;
--drop table #sp_HistoricoAsientos
--exec dbo.sp_XMLAsientosPru

declare @cmd nvarchar(100);
set @cmd= 'D:\WebApps\Cierres\DownloadXml.vbs'
		exec xp_cmdshell @cmd, no_output 
*/
--exec sp_XMLAsientosPru 'CRVSI','2010/007',null,'Ajuste 1'

--select * from historicoasientos where convert(nvarchar(10), fecha_Proceso,103) between '09/05/2010' and '10/05/2010'

END;
