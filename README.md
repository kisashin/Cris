BEGIN TRAN;
EXEC dbo.sp_contabiliza_cardifCentro;
ROLLBACK;


SELECT COUNT(*) FROM TBL_Historico_Movimientos
WHERE fechacontabilizacion IS NULL
  AND llavesiniestro IN (SELECT llavesiniestro FROM TBL_historico_inicial);
