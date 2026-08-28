-- Volver los movimientos a sin contabilizar
UPDATE historicomovimientos 
SET Fechacontabilizacion = NULL 
WHERE archivocargue = 'PRUEBA_COL_AVAL';

-- Dejar una sola fila de control
DELETE FROM controlcierreaval;
INSERT INTO controlcierreaval VALUES (1, GETDATE());

DELETE FROM archivoAsientoAvalXml;
DELETE FROM archivoAsientoCardifXml;
