-- Correr igual en TEST y en PRD, comparar los conteos
SELECT 'Socios_Prod_Siniestros' AS tabla, producto, COUNT(*) AS filas
FROM CardifWP.dbo.Socios_Prod_Siniestros
WHERE producto IN ('2011','2012','2014','2020','2028') GROUP BY producto
UNION ALL
SELECT 'Cobertura_Prod_Xpln_Plz_Cnl', producto, COUNT(*)
FROM CardifWP.dbo.Cobertura_Prod_Xpln_Plz_Cnl
WHERE producto IN ('2011','2012','2014','2020','2028') GROUP BY producto
UNION ALL
SELECT 'Cuentas_Contables_Prod_Siniestros', producto, COUNT(*)
FROM CardifWP.dbo.Cuentas_Contables_Prod_Siniestros
WHERE producto IN ('2011','2012','2014','2020','2028') GROUP BY producto
UNION ALL
SELECT 'PatronxProd_siniestros', producto, COUNT(*)
FROM CardifWP.dbo.PatronxProd_siniestros
WHERE producto IN ('2011','2012','2014','2020','2028') GROUP BY producto
ORDER BY tabla, producto;
