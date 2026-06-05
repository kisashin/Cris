package co.com.bnpparibas.cardif.closingclaims.domain.entity;

import lombok.Getter;
import lombok.Setter;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import javax.persistence.*;
import java.time.LocalDateTime;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Entity
@Table(name = "homologaprod_alfa", schema = "dbo")
public class HomologaPolizaAlfa {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "Id")
    private Integer id;

    @Column(name = "producto")
    private Integer producto;

    @Column(name = "ramo")
    private Integer ramo;

    @Column(name = "nro_poliza")
    private String nroPoliza;

    @Column(name = "\"aplicaVigencia\"")
    private Integer aplicaVigencia;

    @Column(name = "\"fechaInicio\"")
    private LocalDateTime fechaInicio;

    @Column(name = "\"fechaFin\"")
    private LocalDateTime fechaFin;
}
