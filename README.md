-- Productos Aval validos (ramo 7, grupo A)
SELECT TOP 10 PRODUCTO 
FROM Cardifwp.dbo.PRODUCTO_RAMO_PORCENTAJE 
WHERE ramo = 7 AND GRUPO = 'A';

-- Productos Cardif validos (ramo 22, grupo C)
SELECT TOP 10 PRODUCTO 
FROM Cardifwp.dbo.PRODUCTO_RAMO_PORCENTAJE 
WHERE ramo = 22 AND GRUPO = 'C';

-- Cuentas contables por grupo
SELECT GRUPO, COUNT(*) 
FROM Cardifwp.dbo.CUENTAS_CONTABLES_PROD 
GROUP BY GRUPO;
