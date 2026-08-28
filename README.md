-- Devolver los movimientos a sin contabilizar
UPDATE historicomovimientos 
SET Fechacontabilizacion = NULL 
WHERE archivocargue IN ('PRUEBA_COL_CARDIF', 'PRUEBA_COL_COASEG');

-- Vaciar el control, que es lo que dispara la validacion
DELETE FROM controlcierreaval;

-- Limpiar los archivos de la corrida anterior
DELETE FROM archivoAsientoCardifXml;


SELECT COUNT(*) FROM controlcierreaval;




-- Debe dar 0
SELECT COUNT(*) FROM dbo.archivoAsientoCardifXml;

-- Los 10 deben seguir con Fechacontabilizacion NULL
SELECT COUNT(*) 
FROM historicomovimientos 
WHERE archivocargue IN ('PRUEBA_COL_CARDIF', 'PRUEBA_COL_COASEG')
  AND Fechacontabilizacion IS NULL;

  INSERT INTO controlcierreaval VALUES (1, GETDATE());
