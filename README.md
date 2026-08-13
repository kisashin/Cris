Select-String -Path "src\main\java\**\*.java" -Pattern "\x27\x27" -List


-- ¿el SP lo agrega al armar el result set?
select object_definition(object_id('dbo.SP_Reporte_Datos_Siniestros'));

select c.name, t.name as tipo
from sys.columns c join sys.types t on t.user_type_id = c.user_type_id
where c.object_id = object_id('dbo.TBL_Historico_Movimientos') and t.name in ('float','real')
order by c.column_id;
