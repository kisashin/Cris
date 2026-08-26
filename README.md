SELECT COUNT(*) 
FROM historicomovimientos 
WHERE llavesiniestro IN (SELECT llavesiniestro FROM historico_inicial WHERE Aval = 1)
  AND fechacontabilizacion IS NULL 
  AND marcaavalpos IS NULL;
