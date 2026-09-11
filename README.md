SELECT COUNT(*) FROM archivodatos;
SELECT TOP 5 * FROM archivodatos ORDER BY 1 DESC;

-- ¿Las aperturas de tus 5 existen y desde cuando?
SELECT hi.IDCARVAJAL, hi.NumeroSiniestro, hi.Aval
FROM historico_inicial hi
JOIN historicomovimientos hm ON hm.Llavesiniestro = hi.Llavesiniestro
WHERE hm.Fechacontabilizacion IS NULL;
