SELECT tipoMovimiento, COUNT(*) FROM TBL_Historico_Movimientos
WHERE fechacontabilizacion IS NULL GROUP BY tipoMovimiento;

BEGIN TRAN;
EXEC dbo.sp_contabiliza_cardifCentro;
ROLLBACK;
