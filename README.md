package co.com.bnpparibas.cardif.cierres.domain.dtos;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class XmlFileDto {
    private String journalType;
    private String fileName;
    private String content;
}


package co.com.bnpparibas.cardif.cierres.domain.dtos;

import java.util.Date;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class AccountingFileDto {
    private Integer id;
    private String product;
    private String journalType;
    private String fileName;
    private Date generationDate;
}

package co.com.bnpparibas.cardif.cierres.domain.entity;

import java.util.Date;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Table;
import javax.persistence.Temporal;
import javax.persistence.TemporalType;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Table(name = "archivoAsientoReaseguro")
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ArchivoAsientoReaseguro {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id")
    private Integer id;

    @Column(name = "producto")
    private String producto;

    @Column(name = "tipoDiario")
    private String tipoDiario;

    @Column(name = "periodoContable")
    private String periodoContable;

    @Column(name = "nombreArchivo")
    private String nombreArchivo;

    @Column(name = "contenido")
    private String contenido;

    @Column(name = "fechaGeneracion")
    @Temporal(TemporalType.TIMESTAMP)
    private Date fechaGeneracion;

    @Column(name = "usuario")
    private String usuario;
}
