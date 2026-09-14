USE CardifWP;
SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME IN ('Socios_Prod_Siniestros','Cobertura_Prod_Xpln_Plz_Cnl',
                     'Cuentas_Contables_Prod_Siniestros','PatronxProd_siniestros')
  AND COLUMN_NAME LIKE '%prod%'
ORDER BY TABLE_NAME;


SELECT name, type_desc FROM CardifWP.sys.objects
WHERE name LIKE '%Prod_Siniestros%' OR name LIKE '%Cobertura%' OR name LIKE '%Patron%';

USE CardifWP;

SELECT producto, COUNT(*) FROM Socios_Prod_Siniestros
WHERE producto IN ('2011','2012','2014','2020','2028') GROUP BY producto;

SELECT producto, COUNT(*) FROM Cobertura_Prod_Xpln_Plz_Cnl
WHERE producto IN ('2011','2012','2014','2020','2028') GROUP BY producto;

SELECT producto, COUNT(*) FROM Cuentas_Contables_Prod_Siniestros
WHERE producto IN ('2011','2012','2014','2020','2028') GROUP BY producto;

SELECT producto, COUNT(*) FROM PatronxProd_siniestros
WHERE producto IN ('2011','2012','2014','2020','2028') GROUP BY producto;
