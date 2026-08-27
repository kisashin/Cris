insert into #coaseguro exec sp_Gen_Xml_Siniestros_CoaseguroC @periodo2;

if object_id('tempdb..#salidaXml') is not null
begin
	insert into #salidaXml(Familia,Periodo,Pasada,Mv,NombreArchivo,Secuencia,Line)
	select Familia,Periodo,1,Mv,null,Secuencia,Line from #coaseguro;
end;
