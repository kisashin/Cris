SELECT DISTINCT producto FROM Cobertura_Prod_Xpln_Plz_Cnl ORDER BY producto;

SELECT p.producto,
       (SELECT COUNT(*) FROM Socios_Prod_Siniestros s WHERE s.producto = p.producto) AS socios,
       (SELECT COUNT(*) FROM Cobertura_Prod_Xpln_Plz_Cnl c WHERE c.producto = p.producto) AS coberturas
FROM PatronxProd_siniestros p
WHERE p.producto IN (2011, 2012, 2014, 2020, 2028);
