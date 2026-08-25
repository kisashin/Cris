SELECT SUBSTRING(contenido,
                 CHARINDEX('1071.00', contenido) - 750, 950) AS linea
FROM dbo.archivoAsientoCentro
WHERE tipoMovimiento = 'Liberacion';
