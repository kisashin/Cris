USE CardifWP;

-- 1. Socio (solo aporta DESCRIPCION y NIT al asiento)
SELECT * FROM Socios_Prod_Siniestros
WHERE producto IN ('2011','2012','2014','2020','2028') ORDER BY producto;

-- 2. Coberturas: define el peso y el ramo del cruce
SELECT * FROM Cobertura_Prod_Xpln_Plz_Cnl
WHERE producto IN ('2011','2012','2014','2020','2028') ORDER BY producto, cobertura;

-- 3. Patrón y layout: si el producto no está aquí, el SP se va a la rama equivocada
SELECT producto, patron, layout FROM PatronxProd_siniestros
WHERE producto IN ('2011','2012','2014','2020','2028') ORDER BY producto;

-- 4. Cuentas contables, por ramo y tipo de diario (no por producto)
SELECT * FROM Cuentas_Contables_Prod_Siniestros
WHERE tipodiario IN ('LRVSI','CRVSI','SINIE')
  AND ramo IN (SELECT DISTINCT ramo FROM Cobertura_Prod_Xpln_Plz_Cnl
               WHERE producto IN ('2011','2012','2014','2020','2028'))
ORDER BY ramo, tipodiario, ref_transaccion;

-- 5. Periodo contable, que también es configuración
SELECT id, periodocontable, dbo.fFecha2Txt(periodocontable,'/') FROM parametro WHERE id = 4;
