EXEC xp_cmdshell 'dir /B d:\CargueSocios\SALIDA\XML\Procesados\326CO21SR027*.csv';

EXEC xp_cmdshell 'move d:\CargueSocios\SALIDA\XML\Procesados\326CO21SR0272026060105.csv d:\CargueSocios\SALIDA\XML\';
EXEC xp_cmdshell 'dir /B d:\CargueSocios\SALIDA\XML\326CO21SR027*.csv';

EXEC xp_cmdshell 'copy d:\CargueSocios\SALIDA\XML\326CO21SR0272026060105.csv d:\CargueSocios\Pruebas\';
