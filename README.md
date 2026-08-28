SELECT familia, tipoMovimiento, nombreArchivo, cantidadLineas 
FROM archivoAsientoAvalXml ORDER BY familia, tipoMovimiento;

-- Debe dar 93
SELECT COUNT(*) FROM historicomovimientos 
WHERE archivocargue = 'Cargue Col 11 08 2026.xlsx' 
  AND Fechacontabilizacion IS NOT NULL;

-- Debe dar 1
SELECT COUNT(*) FROM controlcierreaval;

-- ¿Se oculto la tabla del reporte? Debe dar 0
SELECT COUNT(*) FROM historicomovimientos 
WHERE Fechacontabilizacion IS NULL AND marcaavalpos IS NULL 
  AND socio IN ('BANCO DE BOGOTA','BANCO AV VILLAS','BANCO DE OCCIDENTE','BANCO POPULAR')
  AND CodProducto NOT IN (SELECT producto FROM dbo.productosnoaval);
