select id_archivo_cargue, nombre, estado, registros, errores, cargadosanterior, porcargar, Id_Modulo
from TBL_Archivo_Cargue order by 1 desc;

select Error, Des_Error, count(*) from TBL_Tmp_Valida_Cargue_Onbase group by Error, Des_Error;


select h.id_archivo_cargue, count(*) as filas
from TBL_Historico_Movimientos h
group by h.id_archivo_cargue order by 1 desc;

select count(*) from TBL_Historico_Inicial;

select top 20 * from TBL_Error order by Id_Error desc;


select count(*) from TBL_Datos_reporte;
select Llavesiniestro, NumeroSiniestro, Socio, Estadosiniestro, Estado_calculado 
from TBL_Datos_reporte where NumeroSiniestro like '0892026A19%';
