 /** DEV: sin copia al file server. Descomentarear para TEST/PROD. */
 exec xp_cmdshell 'Move d:\Carguesocios\Salida\XML\Prueba_Sinie_ReasegExt*.xml d:\Carguesocios\Salida\XML\bk\',no_output;


 select 'd:\Carguesocios\Salida\XML\Prueba_Sinie_ReasegExt_'+mv+convert(varchar(8),getdate(),112)+'.xml' Xml,Rg from #cmd   
 return 0;
