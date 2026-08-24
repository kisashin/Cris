SELECT tipoMovimiento, COUNT(*) FROM TBL_Historico_Movimientos
WHERE fechacontabilizacion IS NULL GROUP BY tipoMovimiento;

BEGIN TRAN;
EXEC dbo.sp_contabiliza_cardifCentro;
ROLLBACK;



SELECT CONVERT(nvarchar(6), FechaMovimiento2, 112) AS periodo,
       CONVERT(nvarchar(6), getdate()-7, 112) AS periodo_del_sp,
       llavesiniestro
FROM TBL_Historico_Movimientos
WHERE fechacontabilizacion IS NULL;
