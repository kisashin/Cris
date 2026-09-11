-- ¿Llegaron al buffer?
SELECT COUNT(*) FROM tmpsiniestros;

-- ¿Que periodo usa Aval vs el de los movimientos?
SELECT CONVERT(nvarchar(6), getdate()-5, 112) AS periodo_aval;

SELECT DISTINCT CONVERT(nvarchar(6), FechaMovimiento2, 112) AS periodo_mov, COUNT(*)
FROM historicomovimientos hm
JOIN historico_inicial hi ON hi.Llavesiniestro = hm.Llavesiniestro
WHERE hm.Fechacontabilizacion IS NULL AND hi.Aval = 1
GROUP BY CONVERT(nvarchar(6), FechaMovimiento2, 112);

-- ¿Llenó la tabla de asientos?
SELECT COUNT(*) FROM HistoricoasientosPru;
