SELECT id_historico_movimiento
FROM dbo.TBL_Historico_Movimientos
WHERE Fechacontabilizacion IS NULL
   OR LTRIM(RTRIM(Fechacontabilizacion)) = '';
