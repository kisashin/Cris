UPDATE historicomovimientos 
SET Fechacontabilizacion = NULL 
WHERE archivocargue = 'Cargue Col 11 08 2026.xlsx';

DELETE FROM archivoAsientoAvalXml;
DELETE FROM archivoAsientoCardifXml;
DELETE FROM controlcierreaval;
DELETE FROM tmp_repavalcierre;
DELETE FROM historicomov_aval;


-- Total pendiente
SELECT COUNT(*) FROM historicomovimientos WHERE Fechacontabilizacion IS NULL;

-- Lo que deberia procesar cada cierre
SELECT hi.Aval, COUNT(*) 
FROM historicomovimientos hm
JOIN historico_inicial hi ON hi.Llavesiniestro = hm.Llavesiniestro
WHERE hm.Fechacontabilizacion IS NULL
GROUP BY hi.Aval;

-- Lo que vera el Excel de Aval
SELECT COUNT(*) FROM historicomovimientos 
WHERE Fechacontabilizacion IS NULL AND marcaavalpos IS NULL 
  AND socio IN ('BANCO DE BOGOTA','BANCO AV VILLAS','BANCO DE OCCIDENTE','BANCO POPULAR')
  AND CodProducto NOT IN (SELECT producto FROM dbo.productosnoaval);


  //////////


  SELECT familia, tipoMovimiento, nombreArchivo, cantidadLineas FROM archivoAsientoAvalXml;

-- Debe dar 93
SELECT COUNT(*) FROM historicomovimientos 
WHERE archivocargue = 'Cargue Col 11 08 2026.xlsx' AND Fechacontabilizacion IS NOT NULL;

-- Debe dar 1
SELECT COUNT(*) FROM controlcierreaval;



SELECT familia, tipoMovimiento, nombreArchivo, cantidadLineas FROM archivoAsientoCardifXml;

-- Debe dar 437
SELECT COUNT(*) FROM historicomovimientos 
WHERE archivocargue = 'Cargue Col 11 08 2026.xlsx' AND Fechacontabilizacion IS NOT NULL;

-- Debe dar 0
SELECT COUNT(*) FROM controlcierreaval;
