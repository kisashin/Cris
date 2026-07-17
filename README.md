SELECT OBJECT_ID('dbo.tblAsientoSiniestros') AS existe_asiento,
       OBJECT_ID('dbo.tblCargaSiniestros')   AS existe_carga;
SELECT DATABASEPROPERTYEX('CardifWP','Collation') AS collation;
