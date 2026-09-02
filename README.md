USE CardifWP;

SELECT SINIESTRO, AVISOS, PAGO_DEFINITIVO
FROM CargaSiniestrosAlfa
WHERE NombreArchivo = '326CO21SR0122026090110.csv'
  AND SINIESTRO = '500001-2026-009005';

SELECT dbo.fFloat('1750,5') AS un_decimal,
       dbo.fFloat('1750,50') AS dos_decimales,
       dbo.fFloat('1750.5') AS punto;
