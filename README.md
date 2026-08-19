SELECT convert(nvarchar(6),FechaMovimiento2,112) periodo,
       tipoMovimiento, count(*) filas, sum(vrmovimiento) valor
FROM TBL_Historico_Movimientos
WHERE fechacontabilizacion is null
  AND llavesiniestro in (select llavesiniestro from TBL_historico_inicial)
GROUP BY convert(nvarchar(6),FechaMovimiento2,112), tipoMovimiento
ORDER BY 1;

SELECT convert(nvarchar(6),FechaMovimiento2,112) periodo,
       tipoMovimiento, count(*) filas, sum(vrmovimiento) valor
FROM historicomovimientos_ext
WHERE fechacontabilizacion is null
  AND llavesiniestro in (select llavesiniestro from historico_inicial_ext)
GROUP BY convert(nvarchar(6),FechaMovimiento2,112), tipoMovimiento
ORDER BY 1;

SELECT tipoMovimiento, count(*)
FROM TBL_Historico_Movimientos
WHERE fechacontabilizacion is null
  AND llavesiniestro in (select llavesiniestro from TBL_historico_inicial)
  AND tipoMovimiento not in ('Aumento Reserva','Reserva Inicial - Aseguradora','Pago',
      'Disminución Reserva','Objetado','Anulado ','Anulado','Disminucion Reserva','objecion','Reversa')
GROUP BY tipoMovimiento;

SELECT count(*) FROM historicomovimientos_ext
WHERE isnull(vrmovimiento,0) = 0 AND fechacontabilizacion is null;

SELECT name, value_in_use FROM sys.configurations WHERE name IN ('xp_cmdshell','show advanced options');
EXEC master.dbo.xp_fileexist 'd:\Carguesocios\Salida\XML\';
SELECT @@servername, SERVERPROPERTY('MachineName');

EXEC sp_helptext 'sp_Gen_Xml_Siniestros_Reaseg_Ext';
EXEC sp_helptext 'sp_agrega_terceros';
EXEC sp_helptext 'sp_Gen_Xml_Terceros_Pagos_Rev';

SELECT Origen, count(*) filas, count(distinct ramo) ramos
FROM cardifwp.dbo.Ramos_Cierre GROUP BY Origen;

SELECT GRUPO, TIPODIARIO, Iva, NATURALEZA, left(Observacion,1) obs, count(*)
FROM cardifwp.dbo.CUENTAS_CONTABLES_PROD
WHERE GRUPO in ('RC','RE')
GROUP BY GRUPO, TIPODIARIO, Iva, NATURALEZA, left(Observacion,1)
ORDER BY GRUPO, TIPODIARIO;

SELECT distinct Formula FROM cardifwp.dbo.CUENTAS_CONTABLES_PROD WHERE GRUPO in ('RC','RE');

SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME IN ('TBL_Asientos_siniestro','tmpsiniestros_ext')
ORDER BY TABLE_NAME, ORDINAL_POSITION;

SELECT marcaavalpos, count(*) FROM historicomovimientos_ext
WHERE fechacontabilizacion is null GROUP BY marcaavalpos;
