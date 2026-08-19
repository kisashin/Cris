SELECT Origen, count(*) FROM cardifwp.dbo.Ramos_Cierre GROUP BY Origen;

SELECT TIPODIARIO, Iva, NATURALEZA, CUENTA, left(Observacion,1) obs, Formula, count(*) filas
FROM cardifwp.dbo.CUENTAS_CONTABLES_PROD
WHERE GRUPO='RC' AND TIPODIARIO in ('CRVSI','LRVSI','SINIE')
GROUP BY TIPODIARIO, Iva, NATURALEZA, CUENTA, left(Observacion,1), Formula
ORDER BY TIPODIARIO, obs, NATURALEZA, CUENTA;
