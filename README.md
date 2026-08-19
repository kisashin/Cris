SELECT TIPODIARIO, left(Observacion,1) obs, NATURALEZA, Iva, Formula, CUENTA
FROM cardifwp.dbo.CUENTAS_CONTABLES_PROD
WHERE GRUPO='RE' AND TIPODIARIO in ('CRVSI','LRVSI','SINIE')
ORDER BY TIPODIARIO, obs, NATURALEZA;

SELECT case when isnull(vrReaseguroRetenido,0)=0 then 'cero/null'
            when vrReaseguroRetenido = vrmovimiento then 'ratio=1'
            else 'parcial' end estado,
       count(*), sum(vrmovimiento)
FROM TBL_Historico_Movimientos
WHERE fechacontabilizacion is null
  AND llavesiniestro in (select llavesiniestro from TBL_historico_inicial)
GROUP BY case when isnull(vrReaseguroRetenido,0)=0 then 'cero/null'
              when vrReaseguroRetenido = vrmovimiento then 'ratio=1'
              else 'parcial' end;
