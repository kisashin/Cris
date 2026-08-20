SELECT MAX(DATALENGTH(Cobertura))/2        AS max_cobertura,
       MAX(DATALENGTH(Nombreasegurado))/2  AS max_nombre,
       MAX(DATALENGTH(Beneficiariopago))/2 AS max_benef
FROM dbo.vw_mov_cardif_ext WITH (NOLOCK);
