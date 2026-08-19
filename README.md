SELECT TABLE_NAME, COLUMN_NAME, CHARACTER_MAXIMUM_LENGTH
FROM INFORMATION_SCHEMA.COLUMNS
WHERE COLUMN_NAME LIKE 'Cobertura%'
  AND TABLE_NAME IN ('tmpsiniestros_ext','historicomovimientos_ext',
                     'TBL_Asientos_siniestro','TBL_Historico_Movimientos');



 SELECT count(*) total, max(len(Cobertura)) largo_max,
       sum(case when len(Cobertura) > 50 then 1 else 0 end) sobre_50
FROM historicomovimientos_ext
WHERE fechacontabilizacion is null
  AND llavesiniestro in (select llavesiniestro from historico_inicial_ext);


BEGIN TRY
  EXEC sp_contabiliza_cardif_ext;
END TRY
BEGIN CATCH
  SELECT ERROR_NUMBER(), ERROR_MESSAGE(), ERROR_LINE();
END CATCH  
