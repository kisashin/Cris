USE CardifWP;
SELECT producto, ramo, cobertura, peso, valor, afectadox
FROM Cobertura_Prod_Xpln_Plz_Cnl WHERE producto IN (2012, 2020);
