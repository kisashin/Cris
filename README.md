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



SELECT COUNT(*) FROM TBL_Historico_Movimientos
WHERE fechacontabilizacion IS NULL
  AND llavesiniestro IN (SELECT llavesiniestro FROM TBL_historico_inicial);

SELECT fechacontabilizacion FROM TBL_Historico_Movimientos
WHERE llavesiniestro = '90044737217162A162-DESEMPLEO';


BEGIN TRAN;
UPDATE TBL_Historico_Movimientos SET fechacontabilizacion = NULL
WHERE CONVERT(nvarchar(6), FechaMovimiento2, 112) = '202608';
-- revisa el conteo, luego COMMIT o ROLLBACK
