SELECT familia, tipoMovimiento, nombreArchivo, cantidadLineas, periodo
FROM archivoAsientoAvalXml ORDER BY familia, tipoMovimiento;

SELECT familia, tipoMovimiento, nombreArchivo, cantidadLineas, periodo
FROM archivoAsientoCardifXml ORDER BY familia, tipoMovimiento;



-- Reparto de lo contabilizado hoy entre Aval y Cardif
SELECT hi.Aval, COUNT(*) 
FROM historicomovimientos hm
JOIN historico_inicial hi ON hi.Llavesiniestro = hm.Llavesiniestro
WHERE hm.archivocargue = 'Cargue Col 11 08 2026.xlsx' 
  AND hm.Fechacontabilizacion = '2026-08-28'
GROUP BY hi.Aval;

-- Y de lo que quedo pendiente
SELECT hi.Aval, COUNT(*) 
FROM historicomovimientos hm
JOIN historico_inicial hi ON hi.Llavesiniestro = hm.Llavesiniestro
WHERE hm.archivocargue = 'Cargue Col 11 08 2026.xlsx' 
  AND hm.Fechacontabilizacion IS NULL
GROUP BY hi.Aval;
