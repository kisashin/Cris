-- 1. ¿Tienen apertura en historico_inicial?
SELECT COUNT(*) 
FROM historicomovimientos hm
LEFT JOIN historico_inicial hi ON hi.Llavesiniestro = hm.Llavesiniestro
WHERE hm.Fechacontabilizacion IS NULL AND hm.Ramo = 22
  AND hi.Llavesiniestro IS NULL;

-- 2. ¿Estan marcados como Aval = 0?
SELECT hi.Aval, COUNT(*)
FROM historicomovimientos hm
JOIN historico_inicial hi ON hi.Llavesiniestro = hm.Llavesiniestro
WHERE hm.Fechacontabilizacion IS NULL AND hm.Ramo = 22
GROUP BY hi.Aval;

-- 3. ¿El producto esta parametrizado?
SELECT DISTINCT hm.CodProducto
FROM historicomovimientos hm
WHERE hm.Fechacontabilizacion IS NULL AND hm.Ramo = 22
  AND hm.CodProducto NOT IN (
    SELECT PRODUCTO FROM Cardifwp.dbo.PRODUCTO_RAMO_PORCENTAJE 
    WHERE ramo = 22 AND GRUPO = 'C');

-- 4. ¿Que tipos de movimiento son?
SELECT Tipomovimiento, COUNT(*)
FROM historicomovimientos
WHERE Fechacontabilizacion IS NULL AND Ramo = 22
GROUP BY Tipomovimiento;
