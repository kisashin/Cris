SELECT SUBSTRING(contenido,
       CHARINDEX('1071.00', contenido),
       1200) AS resto_de_la_linea
FROM dbo.archivoAsientoCentro
WHERE tipoMovimiento = 'Liberacion';
