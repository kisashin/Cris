select id_archivo_cargue, nombre, estado, registros, errores, cargadosanterior, porcargar, Id_Modulo
from TBL_Archivo_Cargue order by 1 desc;

select Error, Des_Error, count(*) from TBL_Tmp_Valida_Cargue_Onbase group by Error, Des_Error;
