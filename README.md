SELECT CAST(BulkColumn AS varchar(max)) AS contenido
FROM OPENROWSET(BULK 'd:\Carguesocios\Salida\XML\bk\Prueba_Sinie_ReasegExt_Constitucion20260820.xml', SINGLE_BLOB) AS x;

EXEC xp_cmdshell 'type "d:\Carguesocios\Salida\XML\bk\Prueba_Sinie_ReasegExt_Constitucion20260820.xml"';
