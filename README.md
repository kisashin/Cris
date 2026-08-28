SELECT socio, COUNT(*) FROM historicomovimientos 
WHERE Fechacontabilizacion IS NULL GROUP BY socio ORDER BY COUNT(*) DESC;

SELECT hi.Aval, COUNT(*) 
FROM historicomovimientos hm
JOIN historico_inicial hi ON hi.Llavesiniestro = hm.Llavesiniestro
WHERE hm.Fechacontabilizacion IS NULL GROUP BY hi.Aval;

SELECT COUNT(*) FROM historicomovimientos 
WHERE Fechacontabilizacion IS NULL AND marcaavalpos IS NULL 
  AND socio IN ('BANCO DE BOGOTA','BANCO AV VILLAS','BANCO DE OCCIDENTE','BANCO POPULAR')
  AND CodProducto NOT IN (SELECT producto FROM dbo.productosnoaval);

SELECT Ramo, COUNT(*) FROM historicomovimientos 
WHERE Fechacontabilizacion IS NULL GROUP BY Ramo ORDER BY Ramo;

SELECT Tipomovimiento, COUNT(*) FROM historicomovimientos 
WHERE Fechacontabilizacion IS NULL GROUP BY Tipomovimiento;

SELECT COUNT(*) FROM historicomovimientos 
WHERE Fechacontabilizacion IS NULL AND tipocoaseguro IS NOT NULL;
