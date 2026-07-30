SELECT COUNT(DISTINCT H1.Llavesiniestro)
FROM TBL_Historico_Movimientos H1
LEFT JOIN tbl_historico_inicial H2 ON H1.Llavesiniestro = H2.Llavesiniestro
WHERE H2.Llavesiniestro IS NULL;
