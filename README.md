SELECT m.tipoMovimiento,
       COUNT(*) total,
       COUNT(i.id_historico_movimiento) pasan_filtro_id
FROM TBL_Historico_Movimientos m
LEFT JOIN (SELECT DISTINCT id_historico_movimiento
           FROM TBL_historico_inicial) i
       ON i.id_historico_movimiento = m.id_historico_movimiento
WHERE m.fechacontabilizacion IS NULL
  AND m.tipoMovimiento IN ('Aumento Reserva','Reserva Inicial - Aseguradora')
GROUP BY m.tipoMovimiento;
