-- 1. El ancho de la columna que revienta (LA CLAVE)
SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'tmpsiniestros_ext'
ORDER BY ORDINAL_POSITION;

-- 2. Compara con el origen
SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'historicomovimientos_ext'
  AND COLUMN_NAME IN ('Cobertura','Nombreasegurado','NumeroSiniestro','NroIdentificacion');

-- 3. ¿Existe allá la cobertura larga?
SELECT max(len(Cobertura)) largo_max, count(distinct Cobertura) variantes
FROM historicomovimientos_ext;

-- 4. ¿El SP es el mismo?
SELECT OBJECT_NAME(m.object_id) sp, LEN(m.definition) tam, o.modify_date
FROM sys.sql_modules m JOIN sys.objects o ON o.object_id = m.object_id
WHERE OBJECT_NAME(m.object_id) IN
  ('sp_Gen_Xml_Siniestros_Reaseg_Ext','sp_contabiliza_cardif_ext',
   'sp_Gen_Xml_Siniestros_ReasegCentro','sp_contabiliza_cardifCentro');
