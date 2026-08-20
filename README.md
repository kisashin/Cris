SELECT COUNT(*) AS listos FROM dbo.historicomovimientos_ext
WHERE fechacontabilizacion IS NULL
  AND llavesiniestro IN (SELECT llavesiniestro FROM historico_inicial_ext);

  EXEC dbo.sp_contabiliza_cardif_ext;

  EXEC xp_cmdshell 'del "d:\Carguesocios\Salida\XML\Prueba_Sinie_ReasegExt_Constitucion20260820.xml"';
