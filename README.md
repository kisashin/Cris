SELECT familia, tipoMovimiento, nombreArchivo, cantidadLineas 
FROM archivoAsientoCardifXml ORDER BY familia, tipoMovimiento;

-- Debe dar 427 (93 de Aval + 334 de Cardif)
SELECT COUNT(*) FROM historicomovimientos 
WHERE archivocargue = 'Cargue Col 11 08 2026.xlsx' 
  AND Fechacontabilizacion IS NOT NULL;

-- Debe dar 0
SELECT COUNT(*) FROM controlcierreaval;
