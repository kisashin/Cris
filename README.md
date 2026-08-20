	begin try drop table ##xmlSin; end try begin catch end catch;

	create table ##xmlSin (
		Tipo_Diario           varchar(10),
		Cuenta                nvarchar(30),
		DC                    varchar(2),
		Referencia            varchar(100),
		Descripcion           nvarchar(50),
		Ramo                  nvarchar(30),
		Producto              nvarchar(20),
		Fecha                 varchar(10),
		nit                   nvarchar(53),
		SinId                 nvarchar(53),
		mv                    varchar(12),
		Corte                 varchar(10),
		Prima                 float,
		Valor                 float,
		idSocio               int,
		Calculo               nvarchar(4000),
		Participacion_Cardif  float,
		Iva                   varchar(2),
		idc                   bigint,
		Line                  varchar(1500),
		id                    int,
		moneda                nvarchar(5)
	);

	insert into ##xmlSin (Tipo_Diario, Cuenta, DC, Referencia, Descripcion, Ramo,
		Producto, Fecha, nit, SinId, mv, Corte, Prima, Valor, idSocio, Calculo,
		Participacion_Cardif, Iva, idc, Line, id, moneda)
	Select     c.TIPODIARIO  collate database_default,c.CUENTA  collate database_default,
	c.NATURALEZA  collate database_default,c.REF_TRANSACCION  collate database_default,
	m.Nombres,cast(m.Ramo as nvarchar),m.Producto,m.Fecha,m.nit,m.SinId,m.mv,m.Corte,
	m.Valor,cast(0 as float),cast(null as int),c.Formula,m.Participacion_Cardif,c.Iva,
	row_number()over(order by c.id),cast(null as varchar(1500)),2,moneda
	from #SinCC m  inner join cardifwp.[dbo].[CUENTAS_CONTABLES_PROD] c  on c.GRUPO='RE' 
	 where   c.TIPODIARIO in('CRVSI','LRVSI','SINIE')
	 AND ((c.IVA='SI' and m.Ramo in(select distinct ramo from cardifwp.dbo.Ramos_Cierre	where iva<>0 and Origen='CO'))
	    or (c.IVA<>'SI' and m.Ramo in(select distinct ramo from cardifwp.dbo.Ramos_Cierre	where iva  =0 and Origen='CO'))
		or (c.IVA='99'))
	 AND(  (m.Mv in('Pago','RevPago') and left(c.Observacion,1) in('3','4'))
	        or(m.Mv='Constitucion' and left(c.Observacion,1) ='1')
	        or(m.Mv  in('Liberacion','Objecion') and left(c.Observacion,1) ='2'));

	 delete ##xmlSin where Prima=0;






    BEGIN TRY

   -- ... todo el bloque existente sin cambios ...
   -- (truncate, 3 inserts, sp_agrega_terceros, sp_Gen_Xml, reversa, terceros)

 END TRY
 BEGIN CATCH
   DECLARE @msg nvarchar(4000) = ERROR_MESSAGE(),
           @sev int = ERROR_SEVERITY(),
           @st  int = ERROR_STATE();
   RAISERROR('sp_contabiliza_cardif_ext: %s', 16, 1, @msg);
   RETURN;
 END CATCH

 update historicomovimientos_ext set fechacontabilizacion = dbo.truncdate(getdate())   
 where   
 llavesiniestro in (select llavesiniestro from historico_inicial_ext)   
 and fechacontabilizacion is null and marcaavalpos is null
