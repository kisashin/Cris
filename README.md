select h.id_archivo_cargue, a.nombre, a.estado, count(*) as filas
from TBL_Historico_Movimientos h
left join TBL_Archivo_Cargue a on a.id_archivo_cargue = h.id_archivo_cargue
group by h.id_archivo_cargue, a.nombre, a.estado
order by h.id_archivo_cargue desc;
