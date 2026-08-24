package co.com.bnpparibas.cardif.closingclaims.domain.entity;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Table;
import java.io.Serializable;
import java.time.LocalDateTime;

@Entity
@Table(name = "archivoAsientoCentro")
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ArchivoAsientoCentro implements Serializable {

    private static final long serialVersionUID = 1L;

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id")
    private Integer id;

    @Column(name = "idLote", length = 36)
    private String idLote;

    @Column(name = "periodo", length = 6)
    private String periodo;

    @Column(name = "tipoMovimiento", length = 50)
    private String tipoMovimiento;

    @Column(name = "nombreArchivo", length = 500)
    private String nombreArchivo;

    @Column(name = "contenido", columnDefinition = "varchar(max)")
    private String contenido;

    @Column(name = "cantidadLineas")
    private Integer cantidadLineas;

    @Column(name = "fechaproceso")
    private LocalDateTime fechaproceso;

    @Column(name = "estado", length = 500)
    private String estado;
}
