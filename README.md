select AfectadoX, SubGrupo from Cardifwp.dbo.x100Grupo 
where grupo='RC' and orden=0 and SubGrupo in ('CSV','BNT');

select Id_Modulo, count(*) from TBL_Archivo_Cargue 
where nombre like 'Cargue CA%' group by Id_Modulo;


Esto en TEST
