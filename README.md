select h.NumeroSiniestro, h.Tipomovimiento, h.Vrmovimiento, h.Fechamovimiento2, h.id_historico_movimiento
from TBL_Historico_Movimientos h
where h.id_archivo_cargue = 707
order by h.NumeroSiniestro;
