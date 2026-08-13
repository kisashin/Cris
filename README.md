select top 5 Direccion, Moneda, Valor, TipoMovimiento, CodigoDeProducto, Des_Error
from TBL_Tmp_Valida_Cargue_Onbase;

select Des_Error, count(*) from TBL_Tmp_Valida_Cargue_Onbase where Error = 1 group by Des_Error order by 2 desc;
