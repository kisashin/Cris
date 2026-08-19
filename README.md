EXEC xp_cmdshell 'bcp "select top 1 name from SiniestrosWp.sys.objects" queryout "d:\Carguesocios\Salida\XML\_test.txt" -dSiniestrosWp -T -S BOGS005DVSQL02 -CRAW -c';
EXEC xp_cmdshell 'dir d:\Carguesocios\Salida\XML\_test.txt';
