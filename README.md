SELECT convert(nvarchar(6),FechaMovimiento2,112) periodo, tipoMovimiento, count(*), sum(vrmovimiento)
FROM TBL_Historico_Movimientos
WHERE fechacontabilizacion is null
  AND llavesiniestro in (select llavesiniestro from TBL_historico_inicial)
GROUP BY convert(nvarchar(6),FechaMovimiento2,112), tipoMovimiento
ORDER BY 1;


SELECT 'Objecion' Mv, Valor_siniestro_objetado, ... Fecha_terminado_siniestro
FROM TBL_Asientos_siniestro
WHERE convert(nvarchar(6),Fecha_terminado_siniestro,112) = ...


*(case when charindex('ParteOtro',Calculo)>0 then 1.0-Participacion_Cardif else 1 end)

SELECT count(*) FROM historicomovimientos_ext
WHERE isnull(vrmovimiento,0) = 0 AND fechacontabilizacion is null;

m.Ramo in (select distinct ramo from cardifwp.dbo.Ramos_Cierre where iva<>0 and Origen='CO')

SELECT Origen, count(*), count(distinct ramo) FROM cardifwp.dbo.Ramos_Cierre GROUP BY Origen;
SELECT Iva, count(*) FROM cardifwp.dbo.CUENTAS_CONTABLES_PROD WHERE GRUPO='RC' GROUP BY Iva;

from #SinCCen m inner join cardifwp.[dbo].[CUENTAS_CONTABLES_PROD] c on c.GRUPO='RC'


EXEC sp_helptext 'sp_Gen_Xml_Siniestros_Reaseg_Ext';   -- ¿mismo Origen='CO'? ¿misma ruta?
EXEC sp_helptext 'sp_agrega_terceros';                  -- Perú lo tiene, Centro no
EXEC sp_helptext 'sp_Gen_Xml_Terceros_Pagos_Rev';       -- genera un XML adicional
