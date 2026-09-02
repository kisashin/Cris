USE CardifWP;

SELECT producto, periodo_contable, descripcion_asiento, tipo_diario,
       estado, COUNT(*) AS movimientos
FROM HistoricoAsientosPru
WHERE tipo_diario IN ('SINIE','LRVSI','CRVSI')
GROUP BY producto, periodo_contable, descripcion_asiento, tipo_diario, estado
ORDER BY producto, periodo_contable DESC;




SELECT DISTINCT producto, descripcion_asiento
FROM HistoricoAsientosPru
WHERE periodo_contable = '2026/002'
  AND tipo_diario IN ('SINIE','LRVSI','CRVSI')
ORDER BY producto;
