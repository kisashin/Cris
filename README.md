EXEC xp_cmdshell 'dir /B d:\CargueSocios\SALIDA\XML\326CO21SR027*.csv';
EXEC xp_cmdshell 'dir /B \\BOGS005DVSQL02\xml';

EXEC dbo.sp_CargaSiniestrosAlfa 2028;

set @Ruta = '\\BOGS005DVSQL02\xml\';
