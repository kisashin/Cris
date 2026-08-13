select h.id_archivo_cargue, a.nombre, a.estado, count(*) as filas
from TBL_Historico_Movimientos h
left join TBL_Archivo_Cargue a on a.id_archivo_cargue = h.id_archivo_cargue
group by h.id_archivo_cargue, a.nombre, a.estado
order by h.id_archivo_cargue desc;


(select max(id_archivo_cargue) from tbl_archivo_cargue 
 where nombre = @nombrearchivo and estado = 'PENDIENTE' and Id_Modulo = (...))


 select top 20 * from TBL_Error order by 1 desc;
select id_archivo_cargue, nombre, estado, registros, errores, cargadosanterior, porcargar, Id_Modulo from TBL_Archivo_Cargue order by 1 desc;
select * from TBL_Modulo;
