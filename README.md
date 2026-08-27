select Familia,Periodo,1 Pasada,Mv,cast(null as nvarchar(100)) NombreArchivo,Secuencia,Line
from #coaseguro
order by Familia,Mv,Secuencia;
