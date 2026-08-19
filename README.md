TRUNCATE TABLE SiniestrosWp.dbo.TBL_Asientos_siniestro;

INSERT INTO SiniestrosWp.dbo.TBL_Asientos_siniestro
(Numero_radicacion_siniestro, Doc_Asegurado, Cobertura_afectada, cod_producto, cod_plan,
 Ramo, Fecha_aviso_Cardif, Reserva_inicial_constituida, Nombre_asegurado, Poliza, id2,
 Participacion_Cardif, Moneda)
SELECT NumeroSiniestro, NroIdentificacion, Cobertura, CodProducto,
       case when isnumeric(CodPlan)=0 then '0'
            when isnumeric(CodPlan)>0 and CodPlan > 9 then '0'
            else isnull(CodPlan,'0') end,
       Ramo, FechaMovimiento2, vrmovimiento,
       upper(left(ltrim(rtrim(Nombreasegurado)),50)), null,
       id_historico_movimiento, 1, Moneda
FROM TBL_Historico_Movimientos
WHERE tipoMovimiento in ('Aumento Reserva','Reserva Inicial - Aseguradora')
  AND id_historico_movimiento in (select id_historico_movimiento from TBL_historico_inicial)
  AND fechacontabilizacion is null;

SELECT count(*) filas, min(Fecha_aviso_Cardif) desde, max(Fecha_aviso_Cardif) hasta
FROM SiniestrosWp.dbo.TBL_Asientos_siniestro;
