-- 1) Tipos reales del result set. Confirma si las fechas y decimales
--    ya vienen como varchar desde el SP (mi hipótesis) o son numéricos.
EXEC sp_describe_first_result_set
     N'EXEC dbo.SP_Reporte_Datos_Siniestros', NULL, 0;

EXEC sp_describe_first_result_set
     N'EXEC dbo.SP_Reporte_Movimientos_Siniestros', NULL, 0;



-- 2) El cuerpo de los tres SP. Me interesa si sp_Genera_Datos_Siniestros
--    usa xp_cmdshell, BULK INSERT, servidores vinculados o BEGIN TRAN propio:
--    eso decide si el @Transactional de generateReport() se queda o se va.
EXEC sp_helptext 'dbo.SP_Reporte_Datos_Siniestros';
EXEC sp_helptext 'dbo.SP_Reporte_Movimientos_Siniestros';
EXEC sp_helptext 'dbo.sp_Genera_Datos_Siniestros';
