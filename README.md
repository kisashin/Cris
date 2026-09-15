select 'COL' origen, nombre, fechaproceso, estado from dbo.archivocargue where fechaproceso >= cast(getdate() as date)
union all
select 'PER', nombre, fechaproceso, estado from dbo.archivocargue_ext where fechaproceso >= cast(getdate() as date)

select 'COL' origen, count(*) filas from dbo.tmponbase
union all
select 'PER', count(*) from dbo.tmponbase_ext

select top 20 NumeroDeIdentificacionDelAsegurado, Direccion, Ciudad, Departamento, Celular, Correo from dbo.tmponbase_ext

select count(distinct h1.Llavesiniestro) from dbo.historicomovimientos_ext h1
left join dbo.historico_inicial_ext h2 on h1.Llavesiniestro = h2.Llavesiniestro
where h2.Llavesiniestro is null