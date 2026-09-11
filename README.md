SELECT DISTINCT archivocargue, marcaavalpos, COUNT(*)
FROM historicomovimientos
WHERE Fechacontabilizacion IS NULL
GROUP BY archivocargue, marcaavalpos;

UPDATE historicomovimientos 
SET marcaavalpos = NULL 
WHERE marcaavalpos IS NOT NULL;

-- Confirmar que no quedan marcados
SELECT COUNT(*) FROM historicomovimientos WHERE marcaavalpos IS NOT NULL;

-- Dejar el registro pendiente y correr la ETL
UPDATE archivodatos SET estado = 'PENDIENTE' WHERE id = 1;
