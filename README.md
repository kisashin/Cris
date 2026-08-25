SELECT NumeroSiniestro, vrmovimiento
FROM TBL_Historico_Movimientos
WHERE fechacontabilizacion IS NULL AND tipoMovimiento = 'Aumento Reserva';
