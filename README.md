SELECT BulkColumn
FROM OPENROWSET(BULK 'd:\Carguesocios\Salida\XML\Sinie_ReasegCentro_Constitucion20260813.xml',
                SINGLE_CLOB) x;
