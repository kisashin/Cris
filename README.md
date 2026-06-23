SELECT id_historico_movimiento
FROM dbo.TBL_Historico_Movimientos
WHERE Fechacontabilizacion IS NULL
   OR LTRIM(RTRIM(Fechacontabilizacion)) = '';


SELECT *
FROM dbo.TBL_Historico_Movimientos
WHERE Fechacontabilizacion IS NULL
   OR LTRIM(RTRIM(Fechacontabilizacion)) = '';



SELECT *
FROM dbo.vw_mov_cardif_cen
WHERE Fechacontabilizacion IS NULL
   OR LTRIM(RTRIM(Fechacontabilizacion)) = '';


EXEC sp_helptext 'dbo.sp_contabiliza_cardifCentro';

SELECT OBJECT_DEFINITION(OBJECT_ID('dbo.sp_contabiliza_cardifCentro')) AS procedure_definition;
