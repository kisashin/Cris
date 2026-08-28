-- Cuantos del cargue quedaron contabilizados hoy
SELECT COUNT(*) FROM historicomovimientos 
WHERE archivocargue = 'Cargue Col 11 08 2026.xlsx' 
  AND Fechacontabilizacion = '2026-08-28';

-- Total del cargue
SELECT COUNT(*) FROM historicomovimientos 
WHERE archivocargue = 'Cargue Col 11 08 2026.xlsx';

-- ¿Se generaron XML?
SELECT COUNT(*) FROM archivoAsientoAvalXml;
SELECT COUNT(*) FROM archivoAsientoCardifXml;
SELECT COUNT(*) FROM controlcierreaval;



UPDATE historicomovimientos 
SET Fechacontabilizacion = NULL 
WHERE archivocargue = 'Cargue Col 11 08 2026.xlsx' 
  AND Fechacontabilizacion = '2026-08-28';
