SELECT COUNT(*) FROM ha 
WHERE descripcion_asiento = '2028_202602' AND producto = '2028';

SELECT DISTINCT ramo FROM Cobertura_Prod_Xpln_Plz_Cnl WHERE producto = 2012;
SELECT DISTINCT ramo FROM Cuentas_Contables_Prod_Siniestros WHERE tipodiario IN ('LRVSI','CRVSI','SINIE');


EXEC xp_cmdshell 'dir /B d:\CargueSocios\SALIDA\XML\Procesados\326CO21SR027*.csv';

EXEC xp_cmdshell 'copy d:\CargueSocios\SALIDA\XML\Procesados\326CO21SR0272026060105.csv d:\CargueSocios\SALIDA\XML\326CO21SR0122026060105.csv';

EXEC xp_cmdshell 'dir /B d:\CargueSocios\SALIDA\XML\326CO21SR012*.csv';

