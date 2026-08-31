--liquibase formatted sql

--changeset j36147:sp_XMLAsientosPru_destino_pantalla stripComments:false dbms:mssql
USE [SiniestrosWp]

GO
SET ANSI_NULLS ON
SET QUOTED_IDENTIFIER ON
GO
--exec SiniestrosWp.dbo.sp_XMLAsientosPru 'SINIE','2023/001','2014','2014_202301'
--exec SiniestrosWp.dbo.sp_XMLAsientosPru 'LRVSI','2015/001',null,'REVSIN'
--exec SiniestrosWp.dbo.sp_XMLAsientosPru 'CRVSI','2015/001',null,'REVSIN'
CREATE OR ALTER PROCEDURE [dbo].[sp_XMLAsientosPru](@Tipo_Diario varchar(50)=null,@Periodo_Contable varchar(10)=null,@Producto Varchar(10)=null,@ajuste varchar(100)=null,@XmlDestino  varchar(10)='SUN'  )
as
declare @cmd nvarchar(max)
declare @ar nvarchar(100)
declare @Prod Varchar(10)
declare @path_server_local varchar(max)
declare @path_server_x varchar(max)
declare @path_server_cierre varchar(300)
declare @param_comand varchar(max)
declare @outputsql2 varchar(max)
declare @outputsql varchar(max)
declare @varxml as varchar(max)
BEGIN
SET NOCOUNT ON

set @Prod=isnull(@Producto,'')
set @Prod=case when left(@Prod,1)='0' then substring(@Prod,2,4) else @Prod end
set @ar=rtrim(ltrim(left(isnull(@ajuste,''),20)))+@Tipo_Diario+'_'
set @ar=@ar+@Prod+replace(@Periodo_Contable,'/0','')+'.XML'
set @ar=replace(@ar,' ','_')


set @path_server_local = (select valor from tbl_parametros_locales where llave = 'Ruta_Local_Server')
set @path_server_x = (select valor from tbl_parametros_locales where llave = 'Ruta_Externa_X')
set @param_comand = (select valor from tbl_parametros_locales where llave = 'comand_exec')
set @path_server_cierre = (select valor from tbl_parametros_locales where llave = 'Ruta_Externa_cierreContable')

update HistoricoAsientosPru set [Nombre_beneficiario]= replace(replace(replace(replace(replace(replace(replace(replace(replace(replace([Nombre_beneficiario],'Á','A'),'É','E'),'Í','I'),'Ó','O'),'Ú','U'),'Ñ','N'),'Ü','U'),'>',''),'<',''),';',' ')
update HistoricoAsientosPru set [Nombre_beneficiario]= replace(replace(replace([Nombre_beneficiario],'Â',''),'¥',''),'¿','')
if len(ltrim(rtrim(@Producto)))<4 set @Producto='0'+ltrim(rtrim(@Producto))
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

--update HistoricoAsientosPru set [Ramo] ='09'
--where [Ramo]='9'  
--and (Periodo_Contable=@Periodo_Contable )

update HistoricoAsientosPru set [NIT_Cedula] ='366964'
where [NIT_Cedula]='E366964'
and (Periodo_Contable=@Periodo_Contable )

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
update HistoricoAsientosPru  set NoSiniestro='' where NoSiniestro is null
-----------------------
 --COSD-8352: Cambiar 19154001 por 19209503
update HistoricoAsientosPru set codigo_cuenta='19209503' 
 where Periodo_Contable=@Periodo_Contable  and codigo_cuenta='19154001'

update HistoricoAsientosPru set codigo_cuenta='51958500' 
 where tipo_diario='RVARC' and Periodo_Contable=@Periodo_Contable
  and codigo_cuenta='51959500' 
  and (cast(producto as int) in(430) OR CAST(socio AS INT) in(1,8,16,19,18,14,33))
------------------
------------------
--Nuevas Cuentas productos



if exists(select 1 from HistoricoAsientosPru where Periodo_Contable=@Periodo_Contable and (cast(producto as int) in(151,150,4101,2902) and tipo_diario in('SINIE','LRVSI','CRVSI')))
begin
 update HistoricoAsientosPru set codigo_cuenta='15600505'   where Periodo_Contable=@Periodo_Contable and  codigo_cuenta='15600501' and (cast(producto as int) in(151,150,4101 , 2902))
 update HistoricoAsientosPru set codigo_cuenta='15600506'   where Periodo_Contable=@Periodo_Contable and  codigo_cuenta='15600502' and (cast(producto as int) in(151,150,4101 , 2902))
 update HistoricoAsientosPru set codigo_cuenta='28810503'   where Periodo_Contable=@Periodo_Contable and  codigo_cuenta='28810500' and (cast(producto as int) in(151,150,4101 , 2902))
 update HistoricoAsientosPru set codigo_cuenta='28959553'   where Periodo_Contable=@Periodo_Contable and  codigo_cuenta='28959500' and (cast(producto as int) in(151,150,4101 , 2902))
 update HistoricoAsientosPru set codigo_cuenta='41020502'   where Periodo_Contable=@Periodo_Contable and  codigo_cuenta='41020500' and (cast(producto as int) in(151,150,4101 , 2902))
 update HistoricoAsientosPru set codigo_cuenta='41027503'   where Periodo_Contable=@Periodo_Contable and  codigo_cuenta='41027500' and (cast(producto as int) in(151,150,4101 , 2902))

 if exists(select 1 from HistoricoAsientosPru where Periodo_Contable=@Periodo_Contable and (cast(producto as int) in(150,4101 , 2902) and tipo_diario in('LRVSI','CRVSI')))
 begin
  update HistoricoAsientosPru set codigo_cuenta='26540503'   where Periodo_Contable=@Periodo_Contable and  codigo_cuenta='26540501' and (cast(producto as int) in(151,150,4101 , 2902))  and tipo_diario='CRVSI'
  update HistoricoAsientosPru set codigo_cuenta='51110504'   where Periodo_Contable=@Periodo_Contable and  codigo_cuenta='51110501' and (cast(producto as int) in(151,150,4101 , 2902))  and tipo_diario='CRVSI'

  update HistoricoAsientosPru set codigo_cuenta='26540503'   where Periodo_Contable=@Periodo_Contable and  codigo_cuenta='26540501' and (cast(producto as int) in(151,150,4101 , 2902))  and tipo_diario='LRVSI'
  update HistoricoAsientosPru set codigo_cuenta='41110503'   where Periodo_Contable=@Periodo_Contable and  codigo_cuenta='41110501' and (cast(producto as int) in(151,150,4101 , 2902))  and tipo_diario='LRVSI'
 end
end--GE


--Bogota 600...
if exists(select 1 from HistoricoAsientosPru where Periodo_Contable=@Periodo_Contable and (cast(producto as int) in(select distinct producto from cardifwp.dbo.producto_td_cierre where socio=10 and left(producto,1)=6) and tipo_diario in('SINIE','LRVSI','CRVSI')))
Begin 

if left(@ajuste,6)='rvASSE'
 begin
  update HistoricoAsientosPru set codigo_cuenta='15082001'   where Periodo_Contable=@Periodo_Contable and tipo_diario='SINIE' and Debito_Credito='D'
  and producto*1 in(select distinct producto from cardifwp.dbo.producto_td_cierre where socio=10 and left(producto,1)=6) 
  update HistoricoAsientosPru set codigo_cuenta='51144000'   where Periodo_Contable=@Periodo_Contable and tipo_diario='SINIE' and Debito_Credito='C'
  and producto*1 in(select distinct producto from cardifwp.dbo.producto_td_cierre where socio=10 and left(producto,1)=6) 
 end
else 
 begin
 update HistoricoAsientosPru set codigo_cuenta='15082001'   where Periodo_Contable=@Periodo_Contable and tipo_diario='SINIE' and Debito_Credito='C'
 and producto*1 in(select distinct producto from cardifwp.dbo.producto_td_cierre where socio=10 and left(producto,1)=6) 
 update HistoricoAsientosPru set codigo_cuenta='51144000'   where Periodo_Contable=@Periodo_Contable and tipo_diario='SINIE' and Debito_Credito='D'
 and producto*1 in(select distinct producto from cardifwp.dbo.producto_td_cierre where socio=10 and left(producto,1)=6) 
end--
End--Bogota 6
------------------
--exec dbo.sp_XMLAsientosPru 'SINIE','2015/001',null,'rvASSE20150130_ALF'
--select * from dbo.tmp_sp_HistoricoAsientosPru order by x_Definir

delete from tmp_sp_HistoricoAsientosPru
insert into tmp_sp_HistoricoAsientosPru([Tipo_Diario],[Periodo_Contable],[Fecha_Transaccion],[Codigo_Cuenta],[Ref_Transaccion],[Descripcion],[Fecha_Vencimiento],[Codigo_Moneda],[Importe_Transaccion],    [Debito_Credito],[Centro_Costos],[Producto],[Ramo],[Impuestos],[Socio],[NIT_Cedula],[Clave_Asesor],[Cobertura],[IdPlan],x_Definir,Descripcion_Asiento,NoSiniestro,[Origen_Diario],fecha_proceso,estado,[Nombre_beneficiario],[CC_beneficiario],[Num_Planilla]) 
 Select distinct [Tipo_Diario],[Periodo_Contable],[Fecha_Transaccion],[Codigo_Cuenta],[Ref_Transaccion],[Descripcion],[Fecha_Vencimiento],[Codigo_Moneda],[Importe_Transaccion],    [Debito_Credito],[Centro_Costos],[Producto],[Ramo],[Impuestos],[Socio],[NIT_Cedula],[Clave_Asesor],[Cobertura],[IdPlan],x_Definir ,Descripcion_Asiento,NoSiniestro,[Origen_Diario],'19000101',estado, [Nombre_beneficiario],[CC_beneficiario],[Num_Planilla] 
 from dbo.HistoricoAsientosPru
 where  Tipo_Diario=@Tipo_Diario and Periodo_Contable=@Periodo_Contable  and  Descripcion_Asiento=@ajuste

--and  x_Definir='422428'
----------------------------Corrige Cuentas de Directas----------------------------------------------------------
update tmp_sp_HistoricoAsientosPru set Cobertura='99999' where tipo_diario in('SINIE','LRVSI','CRVSI') and Cobertura<>'99999' 

update tmp_sp_HistoricoAsientosPru set Codigo_Cuenta='23550000' where  tipo_diario in('SINIE','LRVSI','CRVSI') 
               and producto in(select distinct producto from cardifWp.dbo.prp(nolock) where grupo='C' and socio not in(21,29,41))
               and Codigo_Cuenta='15082001' and Debito_Credito='C'

update tmp_sp_HistoricoAsientosPru set Codigo_Cuenta='51020500' where  tipo_diario in('SINIE','LRVSI','CRVSI') and ramo in('09','24')
               and producto in(select distinct producto from cardifWp.dbo.prp(nolock) where grupo='C' and socio not in(21,29,41))
               and Codigo_Cuenta='51144000' and Debito_Credito='D'
update tmp_sp_HistoricoAsientosPru set Codigo_Cuenta='51021000' where  tipo_diario in('SINIE','LRVSI','CRVSI') and ramo in('31','34')
               and producto in(select distinct producto from cardifWp.dbo.prp(nolock) where grupo='C' and socio not in(21,29,41))
               and Codigo_Cuenta='51144000' and Debito_Credito='D'
                 
update tmp_sp_HistoricoAsientosPru set Codigo_Cuenta='23550000' where  tipo_diario in('SINIE','LRVSI','CRVSI') 
               and producto in(select distinct producto from cardifWp.dbo.prp(nolock) where grupo='C' and socio not in(21,29,41))
               and Codigo_Cuenta='15082001' and Debito_Credito='D'
update tmp_sp_HistoricoAsientosPru set Codigo_Cuenta='51020500' where  tipo_diario in('SINIE','LRVSI','CRVSI') and ramo in('09','24')
               and producto in(select distinct producto from cardifWp.dbo.prp(nolock) where grupo='C' and socio not in(21,29,41))
               and Codigo_Cuenta='51144000' and Debito_Credito='C'
update tmp_sp_HistoricoAsientosPru set Codigo_Cuenta='51021000' where  tipo_diario in('SINIE','LRVSI','CRVSI') and ramo in('31','34')
               and producto in(select distinct producto from cardifWp.dbo.prp(nolock) where grupo='C' and socio not in(21,29,41))
               and Codigo_Cuenta='51144000' and Debito_Credito='C'

if exists(select 1 from HistoricoAsientosPru where Periodo_Contable=@Periodo_Contable 
 and (cast(producto as int) in(select distinct producto from cardifwp.dbo.producto_td_cierre where grupo='A' ) and tipo_diario in('SINIE','LRVSI','CRVSI')))
and charindex('ASSE',@ajuste)>0
Begin 
update tmp_sp_HistoricoAsientosPru set Codigo_Cuenta='15082001' where  tipo_diario in('SINIE','LRVSI','CRVSI') and Codigo_Cuenta='23550000' and charindex('ASSE',@ajuste)>0
               and producto in(select distinct producto from cardifWp.dbo.prp(nolock) where grupo='A' )
update tmp_sp_HistoricoAsientosPru set Codigo_Cuenta='51144000' where  tipo_diario in('SINIE','LRVSI','CRVSI') and Codigo_Cuenta='51020500'and charindex('ASSE',@ajuste)>0
               and producto in(select distinct producto from cardifWp.dbo.prp(nolock) where grupo='A' )
End
                 
--------------------------------------------------------------------------------------

set @varxml = null
set @varxml=(
select top 1
 (select top 1 'S01'as BusinessUnit,'A'as BudgetCode 
  from dbo.tmp_sp_HistoricoAsientosPru as SunSystemsContext FOR XML AUTO,TYPE, ELEMENTS),
  (select  top 1  
   (select  [Tipo_Diario]as JournalType,(substring([Periodo_Contable],6,8)+substring([Periodo_Contable],1,4))as AccountingPeriod,
    replace(case substring([Fecha_Transaccion],5,1)when '/'then (substring([Fecha_Transaccion],9,2)+'/'+substring([Fecha_Transaccion],6,2)+'/'+substring([Fecha_Transaccion],1,4))
     else [Fecha_Transaccion]end
    ,'/','')as TransactionDate,
    [Codigo_Cuenta]as AccountCode,replace(replace(replace(replace(substring([Ref_Transaccion],1,29),'é','e'),'ó','o'),'í','i'),'ñ','n')as TransactionReference,
    
    --***nuevo campo solicitado por contabilidad 08/03/2012
    replace(case substring([Fecha_Transaccion],5,1)when '/'then (substring([Fecha_Transaccion],9,2)+'/'+substring([Fecha_Transaccion],6,2)+'/'+substring([Fecha_Transaccion],1,4))
     else [Fecha_Transaccion]end
    ,'/','')as ValuDate,
    ---*****

    replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(substring([Descripcion],1,49),'é','e'),'ó','o'),'í','i'),'ñ','n'),'Ñ','N'),'Á','A'),'Ó','O'),'¿',''),'¥',''),'Â',''),'Þ','') as Description,
    case substring([Fecha_Vencimiento],5,1)when '/' then (substring([Fecha_Vencimiento],1,2)+'0'+substring([Fecha_Vencimiento],4,1)+substring([Fecha_Vencimiento],6,9))
    else replace([Fecha_Vencimiento],'/','') end as DueDate,[Codigo_Moneda]as CurrencyCode,cast([Importe_Transaccion]as decimal(20,2))as TransactionAmount,
    '2' as TransactionAmountDecimalPlaces,
    '' as BaseAmount,
    '*'as BaseOperator ,
    1 as BaseRate,
    1 as ConversionRate,
    [Debito_Credito]as DebitCredit,[Centro_Costos]as AnalysisCode1,[Producto]as AnalysisCode2,[Ramo]as AnalysisCode3,
    [Impuestos]as AnalysisCode4,[Socio]as AnalysisCode5,[NIT_Cedula]as AnalysisCode6,[Clave_Asesor]as AnalysisCode7,
    [Cobertura]as AnalysisCode8,
    '' as AnalysisCode9 ,case [IdPlan]when ''then '99999' else '99999' end as AnalysisCode10,
    (select top 1 
     case when NoSiniestro is null then '' else left(NoSiniestro,30) end as GeneralDescription1,   --campo NoSiniestro 24/01/2012 
     case when Num_Planilla is null then '' else left(Num_Planilla,30) end as GeneralDescription2,     
     case when CC_beneficiario is null then '' else left(CC_beneficiario,30) end as GeneralDescription3,
     case when Nombre_beneficiario is null then '' else left(Nombre_beneficiario,30) end as GeneralDescription4,
     ''as GeneralDescription5,
     ''as GeneralDescription6,
     ''as GeneralDescription7,
     ''as GeneralDescription8,
     ''as GeneralDescription9,
     ''as GeneralDescription10,
     ''as GeneralDescription11,
     case when isnull(x_Definir,'0')='0' then '' else x_Definir end as GeneralDescription12,
     isnull(left(@ar,30),'') as GeneralDescription13 --Nombre Xml
    from dbo.tmp_sp_HistoricoAsientosPru as DetailLad 
      where ((@Tipo_Diario is null) or (Tipo_Diario=@Tipo_Diario)) and ((@Producto is null) or ( (@Producto='0000' or Producto=@Producto) ))
       and ((@Periodo_Contable is null) or (Periodo_Contable=@Periodo_Contable))
       and ((@ajuste is null) or (Descripcion_Asiento=@ajuste))
      and estado='Pendiente XML' and round(Importe_Transaccion,0)<>0 and DetailLad.NoSiniestro=Line.NoSiniestro  --Validacion para el campo NoSiniestro 24/01/2012
      FOR XML AUTO,TYPE, ELEMENTS ),      
     [Origen_Diario]as JournalSource
   from dbo.tmp_sp_HistoricoAsientosPru as Line 
     where ((@Tipo_Diario is null) or (Tipo_Diario=@Tipo_Diario)) and ((@Producto is null) or ( (@Producto='0000' or Producto=@Producto) ))
       and ((@Periodo_Contable is null) or (Periodo_Contable=@Periodo_Contable))
       and ((@ajuste is null) or (Descripcion_Asiento=@ajuste))
      and estado='Pendiente XML' and round(Importe_Transaccion,0)<>0
    FOR XML AUTO, ROOT ('Ledger'),Type, ELEMENTS)
    from dbo.tmp_sp_HistoricoAsientosPru as Payload 
   where  ((@Tipo_Diario is null) or (Tipo_Diario=@Tipo_Diario)) and ((@Producto is null) or ( (@Producto='0000' or Producto=@Producto) ))
       and ((@Periodo_Contable is null) or (Periodo_Contable=@Periodo_Contable)) 
       and ((@ajuste is null) or (Descripcion_Asiento=@ajuste))
          and estado='Pendiente XML' and round(Importe_Transaccion,0)<>0
   FOR XML AUTO,TYPE, ELEMENTS )
from dbo.tmp_sp_HistoricoAsientosPru 
 where ((@Tipo_Diario is null) or (Tipo_Diario=@Tipo_Diario)) and ((@Producto is null) or ( (@Producto='0000' or Producto=@Producto) ))
       and ((@Periodo_Contable is null) or (Periodo_Contable=@Periodo_Contable)) 
       and ((@ajuste is null) or (Descripcion_Asiento=@ajuste))
       and estado='Pendiente XML' and round(Importe_Transaccion,0)<>0
  FOR XML PATH('SSC') 

)

--?if (select count(*) from PatronxProd_siniestros where producto=@Prod )=0   ---Siniestros reaseguro puro ----@Prod si es nulo ya viene como ''

Begin
 if @varxml is not null and @XmlDestino <> 'PANTALLA'
 begin
  drop table if exists ##VARXML
  --truncate table dbo._##XML_Asiento
  --insert into dbo._##XML_Asiento select '<?xml version="1.0" encoding="UTF-8" ?>'+ @varxml as dataXml
  select '<?xml version="1.0" encoding="UTF-8" ?>'+ @varxml as dataXml into ##VARXML
  --Escribe XML  
  --set @cmd=char(39)+'bcp "select dataXml from SiniestrosWp.dbo._##XML_Asiento" queryout \\bogs005prclfsql\CargueSocios\Salida\XML\'+@ar+' -U bcp -P cobg2008# -c'+char(39)+',no_output'   ---(RUTA DE PRODUCCION)
  
  
  SET @cmd = cast(@param_comand as varchar(50))+''' bcp "select dataXml from ##VARXML" queryout "'+cast(@path_server_local as varchar(50))+cast(@ar as varchar(40))+'" -dSiniestrosWp -T  -S '+@@SERVERNAME+' -T -c -dSiniestrosWp -CRAW'', no_output'


  --set @cmd='EXEC master..xp_cmdshell '+@cmd
  exec(@cmd)    --(COMENTARIAR EN PROD)
  drop table if exists ##VARXML
   --Migracion NEOS 2015/09/12
  --exec Cardifwp.dbo.NEOS_BCP_exec @cmd  --(DESCOMENTARIAR EN PROD)
  --Copia para SUN
  --SET @outputsql = 'net use t: "'+cast(@path_server_cierre as varchar(50))+'" N"cljm\@\{A% /user:AMER\SVCCOLSQLFILESRVCS /persistent:yes'',no_output'
  --exec(@outputsql) 
  
  --exec xp_cmdshell 'dir /s t:\'
  print(@ar)
  print('--------------antes de imprimir el archivo -------')
  SET @outputsql2 = cast(@param_comand as varchar(50))+''' copy /Y '+cast(@path_server_local as varchar(50))+cast(@ar as varchar(40))+' '+cast(@path_server_x as varchar(80))+cast(@ar as varchar(40))+''',no_output'
  exec(@outputsql2)
  print(@cmd)
  --exec (@cmd)
  exec xp_cmdshell 'net use t: /delete',no_output
 end
end
  if @XmlDestino = 'PANTALLA'
  begin
   select @Tipo_Diario Tipo_Diario,
    @ar NombreArchivo,
    case when @varxml is null then null
      else '<?xml version="1.0" encoding="UTF-8" ?>' + @varxml
    end Contenido
   return 0
  end

select @Tipo_Diario Tipo_Diario ,@ar ar,@Periodo_Contable Periodo_Contable,@Producto Producto, @ajuste ajuste, @XmlDestino XmlDestino  
if @varxml is  null select '0'
END
