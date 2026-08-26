--liquibase formatted sql
--changeset j36147:COIMPLUT-35258_Rb_sp_Gen_Xml_Siniestros_ReasegCentro_20260826_01 splitStatements:false

CREATE OR ALTER PROCEDURE [dbo].[sp_Gen_Xml_Siniestros_ReasegCentro](@FC nvarchar(6)) AS
/*
----Proceso para generar archivos XML contables de los movimientos de Siniestro del Reaseguro del Exterior Peru----
-Se parte de los movimientos registrados en la tabla SiniestrosWp.dbo.TBL_Tmp_Siniestros_Centro del mes que corresponden a los prodcutos del Grupo Reaseguro del Exterior 'RC'
exec sp_Gen_Xml_Siniestros_Reaseg_Ext '202005';
*/
BEGIN
	declare @corte datetime=@FC+'01';
	begin try drop table #SinCCen; end try begin catch end catch;
	SELECT 'Constitucion'Mv,Reserva_inicial_constituida Valor,
	       replace(convert(varchar(10),Fecha_aviso_Cardif,103),'/','') Fecha, cod_producto Producto,
		   Numero_radicacion_siniestro SinId,
		   Ramo,left(Doc_Asegurado,10) Nit,
		   Participacion_Cardif,
		   replace(convert(varchar(10),
		   @corte,103),'/','') Corte,
		   upper(Nombre_asegurado) Nombres, Moneda
	into #SinCCen
	FROM TBL_Asientos_siniestro
	WHERE  convert(nvarchar(6),Fecha_aviso_Cardif,112)=  convert(nvarchar(6), @corte,112)

	union all

	SELECT 'Pago'Mv,
	       cuota1,
		   replace(convert(varchar(10),
		   fecha_pago_cuota1,103),'/',''),
		   cod_producto,
		   Numero_radicacion_siniestro,
		   ramo,
		   Doc_Asegurado,Participacion_Cardif,
		   replace(convert(varchar(10),@corte,103),'/',''),
		   upper(Nombre_asegurado) Nombres,
		   Moneda
	FROM TBL_Asientos_siniestro
	WHERE  convert(nvarchar(6),fecha_pago_cuota1,112)=convert(nvarchar(6), @corte,112)
	and    ltrim(rtrim(isnull(Poliza,'')))<>'RevPag'

	union all

	SELECT 'RevPago'    Mv,
	       cuota1,
		   replace(convert(varchar(10),
		   fecha_pago_cuota1,103),'/',''),
		   cod_producto,
		   Numero_radicacion_siniestro,
		   ramo,
		   Doc_Asegurado,
		   Participacion_Cardif,
		   replace(convert(varchar(10),
		   @corte,103),'/',''),
		   upper(Nombre_asegurado) Nombres,
		   Moneda
	FROM TBL_Asientos_siniestro
	WHERE  convert(nvarchar(6),fecha_pago_cuota1,112)=convert(nvarchar(6), @corte,112)
	and    ltrim(rtrim(isnull(Poliza,'')))='RevPag'

	union all

	SELECT 'Liberacion'Mv,
	       Valor_dismin_reserva,
		   replace(convert(varchar(10),
		   fecha_dismi_reserva,103),'/',''),
		   cod_producto,
		   Numero_radicacion_siniestro,
		   ramo,
		   Doc_Asegurado,
		   Participacion_Cardif,
		   replace(convert(varchar(10),@corte,103),'/',''),
		   upper(Nombre_asegurado) Nombres,
		   Moneda
	FROM TBL_Asientos_siniestro
	WHERE  convert(nvarchar(6),fecha_dismi_reserva,112)=convert(nvarchar(6), @corte,112)

	union all

	SELECT 'Objecion' Mv,
	       Valor_siniestro_objetado,
		   replace(convert(varchar(10),
		   Fecha_terminado_siniestro,103),'/',''),
		   cod_producto,
		   Numero_radicacion_siniestro,
		   ramo,
		   Doc_Asegurado,
		   Participacion_Cardif,
		   replace(convert(varchar(10),
		   @corte,103),'/',''),
		   upper(Nombre_asegurado) Nombres,
		   Moneda
	FROM TBL_Asientos_siniestro
	WHERE  convert(nvarchar(6),Fecha_terminado_siniestro,112)=convert(nvarchar(6), @corte,112)
	order by mv,Fecha;

	delete #SinCCen where  isnull(Participacion_Cardif,0)<=0 or sinId is null or producto is null or ramo is null;
	update #SinCCen set nit=sinId where nit is null;

	begin try drop table ##xmlSinCen; end try begin catch end catch;
	Select     c.TIPODIARIO  collate database_default Tipo_Diario,c.CUENTA  collate database_default Cuenta,
	c.NATURALEZA  collate database_default DC,c.REF_TRANSACCION  collate database_default Referencia,
	m.Nombres Descripcion,cast(m.Ramo as nvarchar) as Ramo,m.Producto,m.Fecha,m.nit,m.SinId,m.mv,m.Corte,
	m.Valor Prima,cast(0 as float)Valor,cast(null as int) idSocio,c.Formula Calculo,m.Participacion_Cardif,c.Iva,
	row_number()over(order by c.id) idc,cast(null as varchar(1500))  Line,2 id,moneda
	into  ##xmlSinCen 	from #SinCCen m  inner join cardifwp.[dbo].[CUENTAS_CONTABLES_PROD] c  on c.GRUPO='RC'
	 where   c.TIPODIARIO in('CRVSI','LRVSI','SINIE')
	 AND ((c.IVA='SI' and m.Ramo in(select distinct ramo from cardifwp.dbo.Ramos_Cierre	where iva<>0 and Origen='CO'))
	    or (c.IVA<>'SI' and m.Ramo in(select distinct ramo from cardifwp.dbo.Ramos_Cierre	where iva  =0 and Origen='CO'))
		or (c.IVA='99'))
	 AND(  (m.Mv in('Pago','RevPago') and left(c.Observacion,1) in('3','4'))
	        or(m.Mv='Constitucion' and left(c.Observacion,1) ='1')
	        or(m.Mv  in('Liberacion','Objecion') and left(c.Observacion,1) ='2'));
	 delete ##xmlSinCen where Prima=0;
	update ##xmlSinCen set idSocio=left(Producto,2);
	update ##xmlSinCen set valor=(case DC when 'C' then -1.0 else 1.0 end)*
											    (case when charindex('Prima',Calculo)>0 then abs(Prima) else 1 end)
											   *(case when charindex('ParteCardif',Calculo)>0 then Participacion_Cardif else 1 end)
											   *(case when charindex('ParteOtro',Calculo)>0 then 1.0-Participacion_Cardif else 1 end) ;
	update ##xmlSinCen set  DC=case DC when 'C' then 'D' else 'C' end,valor=-1*valor,Referencia='rv'+Referencia where Mv='RevPago';
	delete ##xmlSinCen where id<>2;
	update ##xmlSinCen set ramo=right('00'+ltrim(rtrim(ramo)),2);
	update ##xmlSinCen set Descripcion=replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(Descripcion,'Á','A'),'É','E'),'Í','I'),'Ó','O'),'Ú','U'),'Ñ','N'),'Ü','U'),'>',''),'<',''),';',' ');
	update ##xmlSinCen set Line='<Line><JournalType>'+Tipo_Diario+'</JournalType><AccountingPeriod>0'+right(Corte,6)+'</AccountingPeriod><TransactionDate>'+Fecha
		+'</TransactionDate><AccountCode>'+Cuenta+'</AccountCode><TransactionReference>'
		+left(case mv when 'Liberacion' then replace(Referencia,'Constitucion','Liberacion') else Referencia end+'('+mv+')',30)+'</TransactionReference>'
		+'<ValuDate>'+Corte+'</ValuDate><Description>'
		+left(Descripcion,30)+'</Description><DueDate>'+Corte+'</DueDate><CurrencyCode>'+Moneda+'</CurrencyCode><TransactionAmount>'
		+ltrim(str(Valor,20,2))+'</TransactionAmount><TransactionAmountDecimalPlaces>2</TransactionAmountDecimalPlaces><BaseAmount/><BaseOperator>*</BaseOperator><BaseRate/><ConversionRate>1</ConversionRate><DebitCredit>'
		+DC+'</DebitCredit><AnalysisCode1>99999</AnalysisCode1><AnalysisCode2>'+replace(str(Producto,4,0),' ','0')+'</AnalysisCode2><AnalysisCode3>' + right('00'+ltrim(rtrim(Ramo)),2) + '</AnalysisCode3><AnalysisCode4>99</AnalysisCode4><AnalysisCode5>'
		+right('00'+idSocio,2)+'</AnalysisCode5><AnalysisCode6>'+ltrim(nit)+'</AnalysisCode6><AnalysisCode7>9999999</AnalysisCode7><AnalysisCode8>99999</AnalysisCode8><AnalysisCode9/><AnalysisCode10>99999</AnalysisCode10><DetailLad><GeneralDescription1>'
		+SinId+'</GeneralDescription1><GeneralDescription2/><GeneralDescription3/><GeneralDescription4/><GeneralDescription5/><GeneralDescription6/><GeneralDescription7/><GeneralDescription8/><GeneralDescription9/><GeneralDescription10/><GeneralDescription11/><GeneralDescription12/><GeneralDescription13>'
		+mv+'</GeneralDescription13></DetailLad><JournalSource>SSC</JournalSource></Line>';

	insert into ##xmlSinCen(line,id,mv)
	 select '<?xml version="1.0" encoding="UTF-8" ?><SSC><SunSystemsContext><BusinessUnit>S01</BusinessUnit><BudgetCode>A</BudgetCode></SunSystemsContext><Payload><Ledger>',0,'enc' union
	 select '</Ledger></Payload></SSC>',3,'pie';

	declare @cmd nvarchar(500),@t nvarchar(500)='exec xp_cmdshell ''bcp "select line from ##xmlSinCen where (id=2 and Mv=''''@mv'''') or id in(0,3) order by id" queryout "d:\Carguesocios\Salida\XML\Sinie_ReasegCentro_@mv'+convert(varchar(8),getdate(),112)+'.xml" -dSiniestrosWp -T  -S '+@@servername+'   -CRAW -c  ''';

	create table #cmd(Rg nvarchar(500),Mv  nvarchar(50));
	set @cmd=REPLACE(@t,'@mv','Constitucion');if (select count(*) from ##xmlSinCen where id=2 and line is not null and Mv='Constitucion')>0 begin insert into #cmd(rg) exec(@cmd);update #cmd set mv='Constitucion' where mv is null;end;
	set @cmd=REPLACE(@t,'@mv','Liberacion');  if (select count(*) from ##xmlSinCen where id=2 and line is not null and Mv='Liberacion')>0   begin insert into #cmd(rg) exec(@cmd);update #cmd set mv='Liberacion' where mv is null;end;
	set @cmd=REPLACE(@t,'@mv','Objecion');    if (select count(*) from ##xmlSinCen where id=2 and line is not null and Mv='Objecion')>0     begin insert into #cmd(rg) exec(@cmd);update #cmd set mv='Objecion' where mv is null;end;
	set @cmd=REPLACE(@t,'@mv','Pago');        if (select count(*) from ##xmlSinCen where id=2 and line is not null and Mv='Pago')>0         begin insert into #cmd(rg) exec(@cmd);update #cmd set mv='Pago' where mv is null;end;
	set @cmd=REPLACE(@t,'@mv','RevPago');     if (select count(*) from ##xmlSinCen where id=2 and line is not null and Mv='RevPago')>0      begin insert into #cmd(rg) exec(@cmd);update #cmd set mv='RevPago' where mv is null;end;
	delete #cmd where isnull(rg,'x') not like '%copied.';
	begin try drop table ##xmlSinCen; end try begin catch end catch;

	return 0;
END;
