USE CardifWP;

-- ¿Las 3 filas quedaron en CargaSiniestrosAlfa?
SELECT COUNT(*) FROM CargaSiniestrosAlfa
WHERE NombreArchivo = '326CO21SR0122026090701.csv';

-- ¿Hay configuración para 2012?
SELECT producto, COUNT(*) AS socios FROM Socios_Prod_Siniestros
WHERE producto IN ('2011','2012','2014','2020','2028') GROUP BY producto;

SELECT producto, COUNT(*) AS coberturas FROM Cobertura_Prod_Xpln_Plz_Cnl
WHERE producto IN ('2011','2012','2014','2020','2028') GROUP BY producto;

SELECT tipodiario, COUNT(*) AS cuentas FROM Cuentas_Contables_Prod_Siniestros
WHERE tipodiario IN ('LRVSI','CRVSI','SINIE') GROUP BY tipodiario;

SELECT id, periodocontable, dbo.fFecha2Txt(periodocontable,'') FROM parametro WHERE id = 4;
