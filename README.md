-- 1. ¿Los ramos de Perú sobreviven el filtro Origen='CO'? (define si el asiento descuadra)
SELECT m.Ramo, count(*) movimientos,
       max(case when rc.ramo is not null then rc.Origen else 'NO EXISTE' end) origen_en_Ramos_Cierre
FROM historicomovimientos_ext m
LEFT JOIN cardifwp.dbo.Ramos_Cierre rc on rc.ramo = m.Ramo
WHERE m.fechacontabilizacion is null
  AND m.llavesiniestro in (select llavesiniestro from historico_inicial_ext)
GROUP BY m.Ramo;

-- 2. ¿Cuántos movimientos de Perú sobreviven el delete de Participacion_Cardif=1?
SELECT case when isnull(vrReaseguroRetenido,0)=0 then 'cero'
            when vrReaseguroRetenido = vrmovimiento then 'ratio=1 (se borra)'
            else 'parcial (sí genera XML)' end estado,
       count(*), sum(vrmovimiento)
FROM historicomovimientos_ext
WHERE fechacontabilizacion is null
  AND llavesiniestro in (select llavesiniestro from historico_inicial_ext)
GROUP BY case when isnull(vrReaseguroRetenido,0)=0 then 'cero'
              when vrReaseguroRetenido = vrmovimiento then 'ratio=1 (se borra)'
              else 'parcial (sí genera XML)' end;


-- 3. Estado de terceros por proceso (mide el daño del UPDATE sin filtro)
SELECT proceso, estado, count(*), count(distinct Identificacion) unicos
FROM historicoterceros GROUP BY proceso, estado ORDER BY 1,2;
