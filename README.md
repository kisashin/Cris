-- ¿Las líneas guardadas coinciden con lo que dice cantidadLineas?
SELECT tipoMovimiento, cantidadLineas,
       (LEN(contenido) - LEN(REPLACE(contenido, '<Line>', ''))) / 6 AS lineas_reales,
       LEN(contenido) AS bytes
FROM dbo.archivoAsientoCentro
ORDER BY id;

-- ¿Están tus siniestros de prueba?
SELECT tipoMovimiento,
       CASE WHEN contenido LIKE '%0902026A195167%' THEN 'SI' ELSE 'NO' END AS constitucion_967,
       CASE WHEN contenido LIKE '%0892026A195311%' THEN 'SI' ELSE 'NO' END AS constitucion_728,
       CASE WHEN contenido LIKE '%0902026A194891%' THEN 'SI' ELSE 'NO' END AS pago_cuatro_cuotas
FROM dbo.archivoAsientoCentro
ORDER BY id;


-- El aumento de 1071 NO debe aparecer en ningún archivo
SELECT tipoMovimiento,
       CASE WHEN contenido LIKE '%1071.00%' THEN 'APARECE' ELSE 'no' END
FROM dbo.archivoAsientoCentro;

-- El Objetado debe estar dentro de Liberacion
SELECT tipoMovimiento,
       (LEN(contenido) - LEN(REPLACE(contenido, 'GeneralDescription13>Objecion', ''))) AS marcas_objecion
FROM dbo.archivoAsientoCentro;


SELECT COUNT(*) FROM dbo.archivoAsientoCentro;
