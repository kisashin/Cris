SELECT COUNT(*) FROM historico_inicial;

SELECT COUNT(*) FROM historico_inicial WHERE Aval = 1;
SELECT COUNT(*) FROM historico_inicial WHERE Aval = 0;

SELECT TOP 5 Llavesiniestro FROM historicomovimientos WHERE Fechacontabilizacion IS NULL;
SELECT TOP 5 Llavesiniestro FROM historico_inicial;
