SELECT COUNT(*) FROM ha 
WHERE descripcion_asiento = '2028_202602' AND producto = '2028';

SELECT DISTINCT ramo FROM Cobertura_Prod_Xpln_Plz_Cnl WHERE producto = 2012;
SELECT DISTINCT ramo FROM Cuentas_Contables_Prod_Siniestros WHERE tipodiario IN ('LRVSI','CRVSI','SINIE');
