select count(*) from Cardifwp.dbo.x100Grupo;
select grupo, orden, SubGrupo, count(*) 
from Cardifwp.dbo.x100Grupo group by grupo, orden, SubGrupo order by 1,2,3;

-- correr en PROD o en el ambiente donde el legacy sí funciona
select * from Cardifwp.dbo.x100Grupo 
where grupo='RC' and orden=0 and SubGrupo in ('CSV','BNT');


select top 20 * from TBL_Error order by Id_Error desc;
select id_archivo_cargue, nombre, estado, registros, errores, cargadosanterior, porcargar, Id_Modulo 
from TBL_Archivo_Cargue order by 1 desc;
select Des_Error, count(*) from TBL_Tmp_Valida_Cargue_Onbase where Error=1 group by Des_Error;
select count(*) from Cardifwp.dbo.x100Grupo where grupo='RC' and orden=0 and SubGrupo in ('CSV','BNT');
