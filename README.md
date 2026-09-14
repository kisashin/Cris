USE CardifWP;

SELECT producto, ramo, cobertura, peso, valor, afectadox
FROM Cobertura_Prod_Xpln_Plz_Cnl
WHERE producto IN ('2011','2020','2028')
ORDER BY producto, ramo;

SELECT producto, ramo FROM Socios_Prod_Siniestros
WHERE producto IN ('2011','2020','2028');
