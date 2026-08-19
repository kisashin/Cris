SELECT count(*) total,
       sum(case when isnull(vrReaseguroRetenido,0)=0 then 1 else 0 end) en_cero,
       min(FechaMovimiento2) desde, max(FechaMovimiento2) hasta
FROM TBL_Historico_Movimientos;
