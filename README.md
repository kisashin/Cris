-- constituciones (Reserva Inicial + Aumento Reserva)
and id_historico_movimiento in (select id_historico_movimiento from TBL_historico_inicial)

-- pagos y disminuciones
and llavesiniestro in (select llavesiniestro from TBL_historico_inicial)

SELECT tipoMovimiento,
       COUNT(*) total,
       SUM(CASE WHEN id_historico_movimiento IN
           (SELECT id_historico_movimiento FROM TBL_historico_inicial)
           THEN 1 ELSE 0 END) pasan_filtro_id
FROM TBL_Historico_Movimientos
WHERE fechacontabilizacion IS NULL
  AND tipoMovimiento IN ('Aumento Reserva','Reserva Inicial - Aseguradora')
GROUP BY tipoMovimiento;
