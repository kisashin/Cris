--liquibase formatted sql

--changeset j36147:sp_Gen_Xml_Siniestros_ReasegCardif_pantalla stripComments:false dbms:mssql
USE [SiniestrosWp]

GO
SET ANSI_NULLS ON
SET QUOTED_IDENTIFIER ON
GO
CREATE OR ALTER procedure  [dbo].[sp_Gen_Xml_Siniestros_ReasegCardif](@FC nvarchar(6)) as 
/*
----Proceso para generar archivos XML contables de los movimientos de Siniestro de reaseguro 
*/
declare @corte datetime
BEGIN
	SET NOCOUNT ON

    -- Se seleccionan los movimientos del periodo
	update tmpsiniestros set Nombre_asegurado=upper(Nombre_asegurado)
	update tmpsiniestros set Nombre_asegurado=replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(Nombre_asegurado,'Á','A'),'É','E'),'Í','I'),'Ó','O'),'Ú','U'),'Ñ','N'),'Ü','U'),'>',''),'<',''),';',' '),
	Cobertura_afectada =replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(Cobertura_afectada,'Á','A'),'É','E'),'Í','I'),'Ó','O'),'Ú','U'),'Ñ','N'),'Ü','U'),'>',''),'<',''),';',' ')
	

	set @corte = @FC+'01'
	
	DROP TABLE IF EXISTS #SinCC


	SELECT 
		id2,
		'Constitucion' Mv,
		Reserva_inicial_constituida Valor, 
		replace(convert(varchar(10),Fecha_aviso_Cardif,103),'/','') Fecha, 
		cod_producto Producto,
		Numero_radicacion_siniestro SinId, 
		Ramo,
		left(Doc_Asegurado,10) Nit,
		Participacion_Cardif,
		replace(convert(varchar(10),@corte,103),'/','') Corte,
		upper(Nombre_asegurado) Nombres,
		Cobertura_afectada Cob,
		ltrim(rtrim([Nombre_beneficiario ])) as NombreBeneficiario,
		ltrim(rtrim(Resultado_siniestro)) as CCbeneficiario,  
		ltrim(rtrim([Num_Planilla])) as NumPlanilla
	into #SinCC 
	FROM tmpsiniestros 
		WHERE  convert(nvarchar(6),Fecha_aviso_Cardif,112)=  convert(nvarchar(6), @corte,112) 
		and ramo in (22) 
		and cod_producto in (select PRODUCTO from Cardifwp.dbo.PRODUCTO_RAMO_PORCENTAJE where ramo = 22 and GRUPO = 'C') 
	union all
	SELECT 
		   id2,
		   'Pago' Mv,
		   cuota1,
		   replace(convert(varchar(10),fecha_pago_cuota1,103),'/',''),        
		   cod_producto,
		   Numero_radicacion_siniestro, 
		   ramo,
		   Doc_Asegurado,
		   Participacion_Cardif,
		   replace(convert(varchar(10),@corte,103),'/',''),
		   upper(Nombre_asegurado) Nombres,
		   Cobertura_afectada,
		   ltrim(rtrim([Nombre_beneficiario ])) as NombreBeneficiario,
		   ltrim(rtrim(Resultado_siniestro)) as CCbeneficiario, 
		   ltrim(rtrim([Num_Planilla ])) as NumPlanilla  
	FROM tmpsiniestros 
		   WHERE  convert(nvarchar(6),fecha_pago_cuota1,112)=convert(nvarchar(6), @corte,112) 
		   and ltrim(rtrim(isnull(Poliza,'')))<>'RevPag'  
		   and ramo in (22) 
		   and cod_producto in (select PRODUCTO from Cardifwp.dbo.PRODUCTO_RAMO_PORCENTAJE where ramo = 22 and GRUPO = 'C')    
	union all
	SELECT	
			id2,
			'RevPago' Mv,
			cuota1,                             
			replace(convert(varchar(10),fecha_pago_cuota1,103),'/',''),        
			cod_producto,
			Numero_radicacion_siniestro, 
			ramo,
			Doc_Asegurado,
			Participacion_Cardif,
			replace(convert(varchar(10),@corte,103),'/',''),
			upper(Nombre_asegurado) Nombres,
			Cobertura_afectada,
			ltrim(rtrim([Nombre_beneficiario ])) as NombreBeneficiario,
			ltrim(rtrim(Resultado_siniestro)) as CCbeneficiario, 
			ltrim(rtrim([Num_Planilla ])) as NumPlanilla 
	FROM tmpsiniestros 
			WHERE  convert(nvarchar(6),fecha_pago_cuota1,112)=convert(nvarchar(6), @corte,112) 
			and ltrim(rtrim(isnull(Poliza,'')))='RevPag'  
			and ramo in (22) 
			and cod_producto in (select PRODUCTO from Cardifwp.dbo.PRODUCTO_RAMO_PORCENTAJE where ramo = 22 and GRUPO = 'C') 		
	union all
	SELECT 
			id2,
			'Liberacion' Mv,
			Valor_dismin_reserva,                
			replace(convert(varchar(10),fecha_dismi_reserva,103),'/',''),      
			cod_producto,
			Numero_radicacion_siniestro, 
			ramo,
			Doc_Asegurado,
			Participacion_Cardif,
			replace(convert(varchar(10),@corte,103),'/',''),
			upper(Nombre_asegurado) Nombres,
			Cobertura_afectada,
			ltrim(rtrim([Nombre_beneficiario ])) as NombreBeneficiario,
			ltrim(rtrim(Resultado_siniestro)) as CCbeneficiario, 
			ltrim(rtrim([Num_Planilla ])) as NumPlanilla 
	FROM tmpsiniestros 
			WHERE  convert(nvarchar(6),fecha_dismi_reserva,112)=convert(nvarchar(6), @corte,112)  
			and ramo in (22) 
			and cod_producto in (select PRODUCTO from Cardifwp.dbo.PRODUCTO_RAMO_PORCENTAJE where ramo = 22 and GRUPO = 'C') 
	union all
	SELECT 
		 id2,
		 'Objecion' Mv,
		 Valor_siniestro_objetado,
		 replace(convert(varchar(10),Fecha_terminado_siniestro,103),'/',''),
		 cod_producto,
		 Numero_radicacion_siniestro, 
		 ramo,
		 Doc_Asegurado,
		 Participacion_Cardif, 
		 replace(convert(varchar(10),@corte,103),'/',''),
		 upper(Nombre_asegurado) Nombres,
		 Cobertura_afectada,
		 ltrim(rtrim([Nombre_beneficiario ])) as NombreBeneficiario,
		 ltrim(rtrim(Resultado_siniestro)) as CCbeneficiario, 
		 ltrim(rtrim([Num_Planilla ])) as NumPlanilla
	FROM tmpsiniestros 
		WHERE  convert(nvarchar(6),Fecha_terminado_siniestro,112)=convert(nvarchar(6), @corte,112)  
		and ramo in (22) 
		and cod_producto in (select PRODUCTO from Cardifwp.dbo.PRODUCTO_RAMO_PORCENTAJE where ramo = 22 and GRUPO = 'C') 
	order by mv,Fecha


	delete #SinCC where  sinId is null or producto is null or ramo is null
	
	update #SinCC set nit=sinId where nit is null

	--Elimina registros con fecha ocurrencia menor a 01/11/2021
	--delete from #SinCC where id2 in (select t.id2 from tmpsiniestros t, historicomovimientos h where t.id2 = h.id and t.ramo=22 and dbo.truncDate(h.Fechaocurrencia) < '20211101')

	

	DROP TABLE IF EXISTS #xmlSin7

	Select  
		c.TIPODIARIO  collate database_default Tipo_Diario,
		c.CUENTA  collate database_default Cuenta,
		c.NATURALEZA  collate database_default DC,
		c.REF_TRANSACCION  collate database_default Referencia,
		m.Nombres Descripcion,
		cast(m.Ramo as nvarchar) as Ramo,
		m.Producto,
		m.Fecha,
		m.nit,
		m.SinId,
		m.mv,
		m.Corte,--c.Grupo_Cuenta, c.Observacion,
		m.Valor Prima,
		cast(0 as float)Valor,
		cast(null as int) idSocio,
		c.Formula Calculo,
		m.Participacion_Cardif,
		c.Iva,
		m.Cob,
		m.NombreBeneficiario, 
		m.CCbeneficiario, 
		NumPlanilla,
		row_number()over(order by c.id) idc,cast(null as nvarchar(max))  Line,
		2 id
	into  #xmlSin7  
	from #SinCC m  
		inner join cardifwp.[dbo].[CUENTAS_CONTABLES_PROD] c  on c.GRUPO='RSGCAR' 
	where  c.TIPODIARIO in('CRVSI','LRVSI','SIREA') and c.formula = 'vOtros'
			AND(  (m.Mv in('Pago','RevPago') and left(c.Observacion,1) in('3','4'))--4. CAUSACIoN PARA PAGO DEL SINIESTRO,3. LIBERACION DE LA RESERVA DE SINIESTROS POR APROBACIONES DE PAGO
	        or(m.Mv='Constitucion' and left(c.Observacion,1) ='1')--1. CONSTITUCIoN O INCREMENTO DE LA RESERVA DE SINIESTROS
	        or(m.Mv  in('Liberacion','Objecion') and left(c.Observacion,1) ='2'))--2. DISMINUCIoN DE LA RESERVA DE SINIESTROS
	 
	 delete #xmlSin7 where Prima=0

	 
	 
	--Se asigna Socio
	update  x set x.idSocio=(select max(socio) from cardifwp.dbo.Producto_TD_Cierre p where p.Producto=x.Producto) from #xmlSin7 x


	--Se calcula el valor del atransaccion(todo el valor es 100% 
	update #xmlSin7 set valor=(case DC when 'C' then -1.0 else 1.0 end)* abs(prima)

	--Se genera las RevPago
	update #xmlSin7 set  DC=case DC when 'C' then 'D' else 'C' end,valor=-1*valor,Referencia='rv'+Referencia where Mv='RevPago'
	--Se crea las <Line> del xml

	delete #xmlSin7 where id<>2 or valor=0
	update #xmlSin7 set NombreBeneficiario = ISNULL(NombreBeneficiario,''),CCbeneficiario = ISNULL(CCbeneficiario,''), NumPlanilla = ISNULL(NumPlanilla,'')
	update #xmlSin7 set ramo=right('00'+ltrim(rtrim(ramo)),2)
	update #xmlSin7 set Line='<Line><JournalType>'+Tipo_Diario+'</JournalType><AccountingPeriod>0'+right(Corte,6)+'</AccountingPeriod><TransactionDate>'+Fecha
		+'</TransactionDate><AccountCode>'+Cuenta+'</AccountCode><TransactionReference>'+left(Referencia,30)+'</TransactionReference><ValuDate>'+Corte+'</ValuDate><Description>'
		+left(Descripcion,50)+'</Description><DueDate>'+Corte+'</DueDate><CurrencyCode>COP</CurrencyCode><TransactionAmount>'
		+ltrim(str(Valor,20,2))+'</TransactionAmount><TransactionAmountDecimalPlaces>2</TransactionAmountDecimalPlaces><BaseAmount/><BaseOperator>*</BaseOperator><BaseRate>1</BaseRate><ConversionRate>1</ConversionRate><DebitCredit>'
		+DC+'</DebitCredit><AnalysisCode1>99999</AnalysisCode1><AnalysisCode2>'+replace(str(Producto,4,0),' ','0')+'</AnalysisCode2><AnalysisCode3>'+Ramo+'</AnalysisCode3><AnalysisCode4>99</AnalysisCode4><AnalysisCode5>'
		+right('00'+idSocio,2)+'</AnalysisCode5><AnalysisCode6>'+right(replace(ltrim(replace(Nit,'0',' ')),' ','0'),10)+'</AnalysisCode6><AnalysisCode7>9999999</AnalysisCode7><AnalysisCode8>99999</AnalysisCode8><AnalysisCode9/><AnalysisCode10>99999</AnalysisCode10><DetailLad><GeneralDescription1>'
		+SinId+'</GeneralDescription1><GeneralDescription2>' + NumPlanilla + '</GeneralDescription2><GeneralDescription3>' +CCbeneficiario + '</GeneralDescription3><GeneralDescription4>' + NombreBeneficiario + '</GeneralDescription4><GeneralDescription5/><GeneralDescription6/><GeneralDescription7/><GeneralDescription8/><GeneralDescription9/><GeneralDescription10/><GeneralDescription11/><GeneralDescription12/><GeneralDescription13>'
		+ left(mv+'-'+cob,29) +'</GeneralDescription13></DetailLad><JournalSource>SSC</JournalSource></Line>'

	--Validar como esta en reaseguro alfa
	---Actualiza Historico reaseguroCardif		
	--delete Hist_Siniestro_ReaseguroCardif where id2 in(select id2 from #SinCC)
	--insert into Hist_Siniestro_ReaseguroCardif(id2,Mv,Valor,Fecha,Producto,SinId,Ramo,Nit,Participacion_Cardif,Corte,Nombres,vTerremoto,vOtros,vDeposito,vBomberos,x100Terremoto,x100Otros,x100Deposito,x100Bomberos,Cob,wProc)
	--select id2,Mv,Valor,Fecha,Producto,SinId,Ramo,Nit,Participacion_Cardif,Corte,Nombres,vTerremoto,vOtros,vDeposito,vBomberos,x100Terremoto,x100Otros,x100Deposito,x100Bomberos,Cob,
	--getdate() wProc from #SinCC

	select 'ReasegCardif' Familia,
	       @FC Periodo,
	       Mv,
	       idc Secuencia,
	       Line
	from #xmlSin7
	where Line is not null
	order by Mv, idc

	return 0
END
