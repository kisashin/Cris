print('entra 1')
if @varxml is not null and @XmlDestino <> 'PANTALLA' select '<?xml version="1.0" encoding="UTF-8" ?>'+ @varxml as dataXml;


if (select count(*) from PatronxProd_siniestros where producto=@Prod )>=0 or @Tipo_Diario='RVARC'   ---Siniestros reaseguro puro ----@Prod si es nulo ya viene como ''

Begin
	if @varxml is not null and @XmlDestino <> 'PANTALLA'
	begin







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



#sp_HistoricoAsientosPru
