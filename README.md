SELECT MAX(DATALENGTH([Cobertura_afectada ]))/2 AS max_cobertura,
       MAX(DATALENGTH(Nombre_asegurado))/2      AS max_nombre,
       MAX(DATALENGTH(Nombre_beneficiario))/2   AS max_benef
FROM dbo.vw_mov_cardif_ext WITH (NOLOCK);


SELECT c.name, t.name AS tipo, c.max_length/2 AS largo
FROM sys.columns c JOIN sys.types t ON t.user_type_id = c.user_type_id
WHERE c.object_id = OBJECT_ID('dbo.historicomovimientos_ext')
  AND c.name LIKE '%ombre%';


  SELECT '[' + name + ']' AS exacto, DATALENGTH(name)/2 AS largo_real
FROM sys.columns WHERE object_id = OBJECT_ID('dbo.tmpsiniestros_ext')
  AND (name LIKE 'Cobertura%' OR name LIKE 'Nombre%');
