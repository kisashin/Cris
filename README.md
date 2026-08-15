USE SiniestrosWp;
GO

select distinct Llavesiniestro into #llaves 
from TBL_Historico_Movimientos where id_archivo_cargue = 707;

DELETE FROM TBL_Historico_Inicial 
WHERE Llavesiniestro IN (select Llavesiniestro from #llaves);

DELETE FROM TBL_Historico_Movimientos WHERE id_archivo_cargue = 707;
DELETE FROM TBL_Archivo_Cargue WHERE id_archivo_cargue = 707;

TRUNCATE TABLE TBL_Tmp_Valida_Cargue_Onbase;
TRUNCATE TABLE TBL_Tmp_Onbase;

drop table #llaves;
GO
