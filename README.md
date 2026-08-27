SELECT COUNT(*) FROM dbo.tmp_repavalcierre;
SELECT COUNT(*) FROM dbo.historicomov_aval;

SELECT COUNT(*) 
FROM historicomovimientos 
WHERE Fechacontabilizacion IS NULL 
  AND marcaavalpos IS NULL 
  AND socio IN ('BANCO DE BOGOTA','BANCO AV VILLAS','BANCO DE OCCIDENTE','BANCO POPULAR')
  AND CodProducto NOT IN (SELECT producto FROM dbo.productosnoaval);
