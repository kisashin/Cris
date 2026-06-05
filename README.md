package co.com.bnpparibas.cardif.closingclaims.infraestructure.repository;

import co.com.bnpparibas.cardif.closingclaims.domain.entity.HomologaPolizaAlfa;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface HomologaPolizaAlfaRepository extends JpaRepository<HomologaPolizaAlfa, Integer> {

    @Query(value = "SELECT Id, producto, ramo, nro_poliza, aplicaVigencia, fechaInicio, fechaFin FROM dbo.homologaprod_alfa WHERE producto = :producto", nativeQuery = true)
    List<HomologaPolizaAlfa> findByProducto(@Param("producto") Integer producto);
}

@Column(name = "aplicaVigencia")
private Integer aplicaVigencia;

@Column(name = "fechaInicio")
private LocalDateTime fechaInicio;

@Column(name = "fechaFin")
private LocalDateTime fechaFin;
