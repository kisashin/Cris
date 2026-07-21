USE CardifWP;

SELECT producto, patron, layout
FROM patronxprod_siniestros
ORDER BY producto;

EXEC xp_cmdshell 'dir /B d:\CargueSocios\Entrada\*.csv';
EXEC xp_cmdshell 'dir /B d:\CargueSocios\SALIDA\XML\*.csv';

EXEC dbo.sp_CargaSiniestros '2011';
EXEC dbo.sp_AsientoSiniestrosAdicionales 1, '2011_202602', '2011';

SELECT * FROM UsuariosCierre;
