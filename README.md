SELECT id_historico_movimiento
FROM dbo.TBL_Historico_Movimientos
WHERE Fechacontabilizacion IS NULL
   OR LTRIM(RTRIM(Fechacontabilizacion)) = ''


EXECUTE dbo.sp_contabiliza_cardifCentro

SELECT *
FROM dbo.vw_mov_cardif_cen


SELECT IDCARVAJAL
FROM dbo.historicomovimientos_ext
WHERE Fechacontabilizacion IS NULL
   OR LTRIM(RTRIM(Fechacontabilizacion)) = ''
 
 
EXECUTE dbo.sp_contabiliza_cardif_ext

findstr /S /I "SiniestrosConnectionString" *.config *.vb

findstr /S /I "BaseContablePeru sp_ EXECUTE SELECT vw_" *.vb

findstr /S /I "BaseContablePeru" *.vb
findstr /S /I "Peru" *.vb
findstr /S /I "contabiliza" *.vb
