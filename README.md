package co.com.bnpparibas.cardif.closingclaims.domain.entity;

import lombok.Getter;
import lombok.Setter;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import javax.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "homologaprod_alfa", schema = "dbo")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class HomologaPolizaAlfa {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "Id", nullable = false, columnDefinition = "INT")
    private Integer id;

    @Column(name = "producto", columnDefinition = "INT")
    private Integer producto;

    @Column(name = "ramo", columnDefinition = "INT")
    private Integer ramo;

    @Column(name = "nro_poliza", length = 100, columnDefinition = "NVARCHAR(100)")
    private String nroPoliza;

    @Column(name = "aplicaVigencia", columnDefinition = "INT")
    private Integer aplicaVigencia;

    @Column(name = "fechaInicio", columnDefinition = "DATETIME")
    private LocalDateTime fechaInicio;

    @Column(name = "fechaFin", columnDefinition = "DATETIME")
    private LocalDateTime fechaFin;
}
