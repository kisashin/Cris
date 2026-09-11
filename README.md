SELECT archivocargue, Fechacontabilizacion, COUNT(*) 
FROM historicomovimientos 
WHERE archivocargue LIKE '%2026%'
GROUP BY archivocargue, Fechacontabilizacion
ORDER BY archivocargue;

-- Lo que ve el filtro del reporte ahora
SELECT COUNT(*) FROM historicomovimientos 
WHERE Fechacontabilizacion IS NULL AND marcaavalpos IS NULL 
  AND socio IN ('BANCO DE BOGOTA','BANCO AV VILLAS','BANCO DE OCCIDENTE','BANCO POPULAR')
  AND CodProducto NOT IN (SELECT producto FROM dbo.productosnoaval);


  SELECT COUNT(*) FROM archivoAsientoAvalXml;
SELECT COUNT(*) FROM controlcierreaval;
