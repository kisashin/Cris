-- Los 10 deben tener fecha
SELECT COUNT(*) AS contabilizados
FROM historicomovimientos 
WHERE Fechacontabilizacion IS NOT NULL 
  AND fechacargue >= CAST(GETDATE() AS DATE);

-- Y no debe quedar ninguno pendiente
SELECT COUNT(*) AS pendientes
FROM historicomovimientos 
WHERE Fechacontabilizacion IS NULL;

-- Detalle por lado
SELECT hi.Aval, hm.Fechacontabilizacion, COUNT(*)
FROM historicomovimientos hm
JOIN historico_inicial hi ON hi.Llavesiniestro = hm.Llavesiniestro
WHERE hm.fechacargue >= CAST(GETDATE() AS DATE)
GROUP BY hi.Aval, hm.Fechacontabilizacion;

-- Archivos generados
SELECT 'Aval' origen, familia, tipoMovimiento, nombreArchivo, cantidadLineas 
FROM archivoAsientoAvalXml
UNION ALL
SELECT 'Cardif', familia, tipoMovimiento, nombreArchivo, cantidadLineas 
FROM archivoAsientoCardifXml;

-- Que la marca quedo limpia
SELECT COUNT(*) FROM historicomovimientos WHERE marcaavalpos IS NOT NULL;
