select Valoraseguradototal, Vrmovimiento, Valordeuda 
from TBL_Datos_reporte where NumeroSiniestro = '0892026A192647';

select Valoraseguradototal, Vrmovimiento 
from TBL_Historico_Movimientos where id_historico_movimiento = 50578735;


select Certificado from TBL_Datos_reporte where NumeroSiniestro = '0892026A192647';



select c.name, t.name as tipo, c.precision, c.scale
from sys.columns c join sys.types t on t.user_type_id = c.user_type_id
where c.object_id = object_id('dbo.TBL_Datos_reporte')
and c.name in ('Valoraseguradototal','Vrmovimiento','Valordeuda','Certificado');
