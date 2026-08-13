select c.name, t.name as tipo
from sys.columns c join sys.types t on t.user_type_id = c.user_type_id
where c.object_id = object_id('dbo.TBL_Datos_reporte') and t.name in ('float','real')
order by c.column_id;
