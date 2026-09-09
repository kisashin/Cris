-- ¿Que periodo esta usando Cardif?
SELECT fecha, CONVERT(nvarchar(6), fecha, 112) AS periodo FROM controlcierreaval;

-- ¿Cuantos de los 90 tienen apertura?
SELECT COUNT(*) 
FROM historicomovimientos hm
JOIN historico_inicial hi ON hi.Llavesiniestro = hm.Llavesiniestro
WHERE hm.Fechacontabilizacion IS NULL AND hi.Aval = 0 AND hm.Ramo = 22;

-- ¿El producto esta parametrizado para ramo 22 grupo C?
SELECT DISTINCT hm.CodProducto
FROM historicomovimientos hm
WHERE hm.Fechacontabilizacion IS NULL AND hm.Ramo = 22
  AND hm.CodProducto NOT IN (
    SELECT PRODUCTO FROM Cardifwp.dbo.PRODUCTO_RAMO_PORCENTAJE 
    WHERE ramo = 22 AND GRUPO = 'C');
