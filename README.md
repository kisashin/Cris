USE CardifWP;
GO
INSERT INTO dbo.x100Grupo (Grupo, SubGrupo, Descripcion, Nit_Compania, x100_Participa, Fecha_Desde, Orden, AfectadoX, Valor, basex100)
VALUES
 ('RC','CSV','CV Agricola','900200435-3',1,'2022-02-05',0,'9001',1,NULL),
 ('RC','CSV','CV Agricola','900200435-3',1,'2022-02-05',0,'9002',1,NULL),
 ('RC','CSV','CV Agricola','900200435-3',1,'2022-02-05',0,'9004',1,NULL),
 ('RC','BNT','CV Banitsmo','633197-1-456744',1,'2023-01-05',0,'8901',1,NULL),
 ('RC','BNT','CV Banitsmo','633197-1-456744',1,'2023-01-05',0,'8902',1,NULL),
 ('RC','BNT','CV Banitsmo','633197-1-456744',1,'2023-01-05',0,'8905',1,NULL);
GO

USE SiniestrosWp;
GO
UPDATE dbo.TBL_Archivo_Cargue SET estado='ELIMINADO' WHERE id_archivo_cargue = 706;
TRUNCATE TABLE dbo.TBL_Tmp_Valida_Cargue_Onbase;
TRUNCATE TABLE dbo.TBL_Tmp_Onbase;
GO

select tipoasenda, tipocardif from homologatipomov
where tipoasenda in ('APERTURA INICIAL','AUMENTO','PAGO DE CUOTA','REVERSA DE CUOTA');

select estado_onbase, estado_cardif, subestado_cardif from homologatipoestados
where estado_onbase in ('ANALISIS','REVISION DE PAGO','OBJECION RATIFICADA TERMINADA','SUSPENSO','PAGO ACEPTADO TERMINADO','PAGO CUOTAS POR PROGRAMAR');

select tipomovimiento, agrupacion from Agrupamovimiento
where tipomovimiento in ('APERTURA INICIAL','AUMENTO','PAGO DE CUOTA','REVERSA DE CUOTA');





package co.com.bnpparibas.cardif.closingclaims.domain.entity;

import lombok.*;

import javax.persistence.Column;
import javax.persistence.EmbeddedId;
import javax.persistence.Entity;
import javax.persistence.Table;
import java.io.Serializable;

@Entity
@Table(name = "TBL_Archivo_Cargue")
@Getter
@Setter
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class ArchivoCargueTBL implements Serializable {

    private static final long serialVersionUID = 1L;

    @EmbeddedId
    private FileLoadId id;

    @Column(name = "estado", length = 500)
    private String estado;

    @Column(name = "registros")
    private Integer registros;

    @Column(name = "errores")
    private Integer errores;

    @Column(name = "cargadosanterior")
    private Integer cargadosanterior;

    @Column(name = "porcargar")
    private Integer porcargar;

    @Column(name = "id_Modulo")
    private Integer idModulo;

}
