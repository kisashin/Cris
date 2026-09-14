USE CardifWP;

SELECT 'Socios_Prod_Siniestros' AS tabla, producto, COUNT(*) AS filas
FROM Socios_Prod_Siniestros WHERE producto IN ('2011','2012','2014','2020','2028') GROUP BY producto
UNION ALL
SELECT 'Cobertura_Prod_Xpln_Plz_Cnl', producto, COUNT(*)
FROM Cobertura_Prod_Xpln_Plz_Cnl WHERE producto IN ('2011','2012','2014','2020','2028') GROUP BY producto
UNION ALL
SELECT 'PatronxProd_siniestros', producto, COUNT(*)
FROM PatronxProd_siniestros WHERE producto IN ('2011','2012','2014','2020','2028') GROUP BY producto
ORDER BY tabla, producto;


USE CardifWP;
SELECT * FROM Socios_Prod_Siniestros WHERE producto = '2011';
SELECT * FROM Cobertura_Prod_Xpln_Plz_Cnl WHERE producto = '2011';
SELECT producto, patron, layout FROM PatronxProd_siniestros WHERE producto = '2011';
