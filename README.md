/* =====================================================================
   EXTRACCION PARA LEVANTAMIENTO - Asientos Siniestros Cardif
   ---------------------------------------------------------------------
   BD objetivo : la de CardifWPConnectionString (ejecutar en AMBIENTE TEST)
   Como correr : SSMS > Ctrl+T (resultados a texto) > ejecutar por seccion
                 > guardar la salida completa como .txt y enviarla.

   Anti-truncado: para los cuerpos de SP se usa sp_helptext, que devuelve
   el texto completo linea a linea (OBJECT_DEFINITION se trunca en la
   grilla). Alternativa mas limpia para traer TODO de una sola vez:
   clic derecho en la BD > Tasks > Generate Scripts > seleccionar los
   SPs y tablas de la seccion 1 > generar un unico .sql y enviar ese.

   PII: ninguna consulta de este script devuelve datos personales de
   asegurados. NO agregar SELECT * sobre tmpSiniestros / dc / documento
   sin enmascarar nombre, documento, direccion, telefonos, celular y
   fecha de nacimiento.
   ===================================================================== */

-- ---------------------------------------------------------------------
-- 0. Contexto del servidor. La version de SQL importa para saber que
--    puede estar usando el SP (OPENROWSET, BULK INSERT, FOR XML,
--    sp_send_dbmail) y que restricciones tendra la migracion.
--    Tambien confirma si es la misma instancia de ws-closing-claims.
-- ---------------------------------------------------------------------
SELECT @@SERVERNAME AS servidor, DB_NAME() AS base_de_datos, @@VERSION AS version_sql;

-- ---------------------------------------------------------------------
-- 1. Inventario: que existe y cuando se modifico por ultima vez.
--    modify_date reciente = alguien lo toco hace poco; relevante para
--    congelar alcance. Si sp_InsertarTmpSiniestros NO aparece aqui,
--    la validacion no esta comentada: esta borrada. Anotarlo.
-- ---------------------------------------------------------------------
SELECT o.name, o.type_desc, o.create_date, o.modify_date
FROM sys.objects o
WHERE o.name IN (
    -- SPs del flujo SINI (prioridad alta)
    'sp_asientosSiniestros', 'sp_XMLAsientosPru', 'ListaArhivos',
    'sp_InsertarTmpSiniestros',
    -- SPs compartidos con EMIDI/ANUDI/REVEM (definen la frontera de alcance)
    'sp_PuedeGenerarInterfaz_XML', 'sp_AsientosxSocio_NewXML',
    'sp_ProductosRegistrados_XML', 'sp_ProductosxRegistrarEmiCan_XML',
    'sp_ProduccionNormalPlus',
    -- Tablas
    'tmpSiniestros', 'historicoasientospru', 'Parametro',
    'usuariosCierre', 'documento', 'dc', 'Producto'
)
ORDER BY o.type_desc, o.name;

-- ---------------------------------------------------------------------
-- 2. Cuerpos de los SP. Esto ES la especificacion del modulo.
--    Ejecutar uno por uno y enviar la salida completa de cada uno.
-- ---------------------------------------------------------------------
EXEC sp_helptext 'dbo.sp_asientosSiniestros';     -- PRIORIDAD 1: modos 0-7, uso de tmpSiniestros, sobrecarga del 4o parametro
EXEC sp_helptext 'dbo.sp_XMLAsientosPru';         -- PRIORIDAD 2: generacion del XML, semantica SINIE/LRVSI/CRVSI
EXEC sp_helptext 'dbo.ListaArhivos';              -- PRIORIDAD 2: correo (destinatarios, mecanismo, cuerpo)
EXEC sp_helptext 'dbo.sp_InsertarTmpSiniestros';  -- puede fallar si fue borrado: reportar el error tal cual

-- Solo si el alcance termina incluyendo RepCierre completo (EMIDI/ANUDI/REVEM),
-- descomentar y ejecutar:
-- EXEC sp_helptext 'dbo.sp_PuedeGenerarInterfaz_XML';
-- EXEC sp_helptext 'dbo.sp_AsientosxSocio_NewXML';
-- EXEC sp_helptext 'dbo.sp_ProductosRegistrados_XML';
-- EXEC sp_helptext 'dbo.sp_ProductosxRegistrarEmiCan_XML';
-- EXEC sp_helptext 'dbo.sp_ProduccionNormalPlus';

-- ---------------------------------------------------------------------
-- 3. Dependencias: quien mas lee/escribe estas tablas y quien mas llama
--    a estos SP. Cualquier objeto que aparezca aqui y NO este en el .vb
--    (otro SP, una vista, un trigger, otro sistema) es alcance oculto.
-- ---------------------------------------------------------------------
SELECT DISTINCT
    d.referenced_entity_name      AS objeto_referenciado,
    OBJECT_NAME(d.referencing_id) AS quien_lo_usa,
    o.type_desc
FROM sys.sql_expression_dependencies d
JOIN sys.objects o ON o.object_id = d.referencing_id
WHERE d.referenced_entity_name IN
      ('tmpSiniestros', 'historicoasientospru',
       'sp_asientosSiniestros', 'sp_XMLAsientosPru', 'ListaArhivos')
ORDER BY objeto_referenciado, quien_lo_usa;

-- ---------------------------------------------------------------------
-- 4. Jobs de SQL Agent que toquen el flujo. Requiere permiso de lectura
--    en msdb; si falla, pedirselo al DBA (vale la pena). Clave para dos
--    cosas: si el modo 7 del SP (carga por ruta de archivo, boton OnBase
--    oculto) lo consume algo automatizado, y si hay pasos del cierre
--    que corren por job y no por la pantalla.
-- ---------------------------------------------------------------------
SELECT j.name AS job, j.enabled, s.step_id, s.step_name, s.command
FROM msdb.dbo.sysjobs j
JOIN msdb.dbo.sysjobsteps s ON s.job_id = j.job_id
WHERE s.command LIKE '%Siniestros%'
   OR s.command LIKE '%XMLAsientos%'
   OR s.command LIKE '%ListaArhivos%'
   OR s.command LIKE '%Entrada\Sini%';

-- ---------------------------------------------------------------------
-- 5. Estructura de las tablas. En tmpSiniestros se esperan 45 columnas
--    (44 del layout + 1 que el insert del .vb deja en null): identificar
--    que es esa columna 45. En Parametro interesa el tipo de dato de
--    PeriodoContable (fecha completa vs varchar).
-- ---------------------------------------------------------------------
SELECT t.name AS tabla, c.column_id, c.name AS columna, ty.name AS tipo,
       c.max_length, c.precision, c.scale, c.is_nullable, c.is_identity
FROM sys.columns c
JOIN sys.tables t ON t.object_id = c.object_id
JOIN sys.types ty ON ty.user_type_id = c.user_type_id
WHERE t.name IN ('tmpSiniestros', 'historicoasientospru', 'Parametro',
                 'usuariosCierre', 'documento', 'dc', 'Producto')
ORDER BY t.name, c.column_id;

-- ---------------------------------------------------------------------
-- 6. Triggers sobre las tablas del flujo: logica invisible desde el .vb.
--    Si devuelve filas, correr sp_helptext por cada trigger y enviarlo.
-- ---------------------------------------------------------------------
SELECT OBJECT_NAME(t.parent_id) AS tabla, t.name AS trigger_name, t.is_disabled
FROM sys.triggers t
WHERE t.parent_id IN (OBJECT_ID('dbo.tmpSiniestros'),
                      OBJECT_ID('dbo.historicoasientospru'),
                      OBJECT_ID('dbo.documento'),
                      OBJECT_ID('dbo.dc'));

-- ---------------------------------------------------------------------
-- 7. Datos de contexto (sin PII)
-- ---------------------------------------------------------------------

-- 7a. El registro que gobierna el periodo contable activo
SELECT * FROM dbo.Parametro WHERE id = 4;

-- 7b. Semantica real de SINIE / LRVSI / CRVSI, formato del periodo y
--     descripciones de ajuste historicas (lo que alimenta el dropdown
--     "Comentario" y evidencia de cuantos reprocesos ha habido)
SELECT TOP 30 Tipo_Diario, periodo_contable, descripcion_asiento,
       COUNT(*) AS registros
FROM dbo.historicoasientospru
WHERE Tipo_Diario IN ('SINIE', 'LRVSI', 'CRVSI')
GROUP BY Tipo_Diario, periodo_contable, descripcion_asiento
ORDER BY periodo_contable DESC, Tipo_Diario;

-- 7c. Roles reales del sistema, sin listar usuarios
SELECT perfil, COUNT(*) AS usuarios
FROM dbo.usuariosCierre
GROUP BY perfil;

-- ---------------------------------------------------------------------
-- 8. (Opcional, suele requerir permisos elevados) Confirmar si el motor
--    tiene Database Mail configurado; el cuerpo de ListaArhivos dira si
--    usa sp_send_dbmail, pero esto confirma que el perfil existe.
-- ---------------------------------------------------------------------
-- SELECT name FROM msdb.dbo.sysmail_profile;
