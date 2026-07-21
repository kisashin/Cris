EXEC xp_cmdshell 'dir d:\CargueSocios\Salida';
EXEC xp_cmdshell 'dir d:\CargueSocios\Salida\XML';
EXEC xp_cmdshell 'dir d:\CargueSocios\Entrada';
EXEC xp_cmdshell 'dir d:\CargueSocios\Pruebas';

EXEC sp_helptext 'dbo.sp_CargaSiniestrosAlfa';

EXEC xp_cmdshell 'copy c:\archivo_prueba.csv d:\CargueSocios\Salida\XML\326CO21SR026prueba.csv';
