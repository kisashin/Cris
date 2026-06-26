EXEC sp_describe_first_result_set
    N'SELECT * FROM dbo.vw_mov_cardif_cen', NULL, 0;

SELECT IDCARVAJAL, COUNT(*)
FROM dbo.vw_mov_cardif_cen
GROUP BY IDCARVAJAL
HAVING COUNT(*) > 1;
