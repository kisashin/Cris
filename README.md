SELECT name FROM sys.databases ORDER BY name;
SELECT @@SERVERNAME, SERVERPROPERTY('MachineName'), SERVERPROPERTY('InstanceName');
SELECT name, data_source FROM sys.servers WHERE server_id > 0;

SELECT TIPODIARIO, Iva, NATURALEZA, CUENTA, left(Observacion,1) obs, Formula, count(*) filas
FROM cardifwp.dbo.CUENTAS_CONTABLES_PROD
WHERE GRUPO='RC' AND TIPODIARIO in ('CRVSI','LRVSI','SINIE')
GROUP BY TIPODIARIO, Iva, NATURALEZA, CUENTA, left(Observacion,1), Formula
ORDER BY TIPODIARIO, obs, NATURALEZA, CUENTA;
