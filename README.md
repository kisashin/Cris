TRUNCATE TABLE SiniestrosWp.dbo.tmpsiniestros_ext;

INSERT INTO SiniestrosWp.dbo.tmpsiniestros_ext
(Numero_radicacion_siniestro, Doc_Asegurado, Cobertura_afectada, cod_producto, cod_plan,
 Ramo, Fecha_aviso_Cardif, Reserva_inicial_constituida, Nombre_asegurado, Poliza, id2,
 Participacion_Cardif, Moneda)
SELECT NumeroSiniestro, NroIdentificacion, Cobertura, CodProducto,
       case when isnumeric(CodPlan)=0 then '0'
            when isnumeric(CodPlan)>0 and CodPlan > 9 then '0'
            else isnull(CodPlan,'0') end,
       Ramo, FechaMovimiento2, vrmovimiento,
       upper(left(ltrim(rtrim(Nombreasegurado)),50)), null, id,
       vrReaseguroRetenido/vrmovimiento, Moneda
FROM historicomovimientos_ext
WHERE tipoMovimiento in ('Aumento Reserva','Reserva Inicial - Aseguradora')
  AND llavesiniestro in (select llavesiniestro from historico_inicial_ext)
  AND fechacontabilizacion is null;

SELECT count(*) filas,
       min(Fecha_aviso_Cardif) desde, max(Fecha_aviso_Cardif) hasta,
       min(Participacion_Cardif) part_min, max(Participacion_Cardif) part_max
FROM SiniestrosWp.dbo.tmpsiniestros_ext;


EXEC sp_Gen_Xml_Siniestros_Reaseg_Ext '202606';
EXEC xp_cmdshell 'dir d:\Carguesocios\Salida\XML\Prueba_Sinie_ReasegExt_*';


EXEC xp_cmdshell 'dir \\amcobgfp01wp\Soluciones\T_CONTABILIDAD\Siniestros\Interfaz\';
