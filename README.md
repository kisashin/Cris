EXEC xp_cmdshell 'del "d:\Carguesocios\Salida\XML\Terceros_20260819_PERU_224850_.xml"';

EXEC xp_cmdshell 'dir d:\Carguesocios\Salida\XML\Terceros_*.xml';


EXEC xp_cmdshell 'move "d:\Carguesocios\Salida\XML\Terceros_20260819_PERU_224850_.xml" "d:\Carguesocios\Salida\XML\bk\"';
