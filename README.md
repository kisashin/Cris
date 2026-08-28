-- 1. Cuantos movimientos entraron
SELECT COUNT(*) FROM historicomovimientos WHERE Fechacontabilizacion IS NULL;

-- 2. Como quedaron los socios (esto es lo que mas me importa)
SELECT socio, COUNT(*) FROM historicomovimientos 
WHERE Fechacontabilizacion IS NULL GROUP BY socio ORDER BY COUNT(*) DESC;

-- 3. Reparto Aval / Cardif
SELECT hi.Aval, COUNT(*) 
FROM historicomovimientos hm
JOIN historico_inicial hi ON hi.Llavesiniestro = hm.Llavesiniestro
WHERE hm.Fechacontabilizacion IS NULL GROUP BY hi.Aval;

-- 4. Lo que va a ver el reporte de Aval
SELECT COUNT(*) FROM historicomovimientos 
WHERE Fechacontabilizacion IS NULL AND marcaavalpos IS NULL 
  AND socio IN ('BANCO DE BOGOTA','BANCO AV VILLAS','BANCO DE OCCIDENTE','BANCO POPULAR')
  AND CodProducto NOT IN (SELECT producto FROM dbo.productosnoaval);

-- 5. Ramos y tipos de movimiento
SELECT Ramo, COUNT(*) FROM historicomovimientos 
WHERE Fechacontabilizacion IS NULL GROUP BY Ramo ORDER BY Ramo;

SELECT Tipomovimiento, COUNT(*) FROM historicomovimientos 
WHERE Fechacontabilizacion IS NULL GROUP BY Tipomovimiento;

-- 6. Coaseguro
SELECT COUNT(*) FROM historicomovimientos 
WHERE Fechacontabilizacion IS NULL AND tipocoaseguro IS NOT NULL;
