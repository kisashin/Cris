SELECT COUNT(*) FROM Socios_Prod_Siniestros WHERE producto = 2028;
SELECT COUNT(*) FROM Cobertura_Prod_Xpln_Plz_Cnl WHERE producto = 2028;
SELECT COUNT(*) FROM Cuentas_Contables_Prod_Siniestros WHERE tipodiario IN ('LRVSI','CRVSI','SINIE');

SELECT TOP 5 NombreArchivo, FechaProceso, COUNT(*) AS filas
FROM CargaSiniestrosAlfa
WHERE producto = 2028
GROUP BY NombreArchivo, FechaProceso
ORDER BY FechaProceso DESC;
