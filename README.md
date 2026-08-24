package co.com.bnpparibas.cardif.closingclaims.infraestructure.repository;

import co.com.bnpparibas.cardif.closingclaims.domain.entity.ArchivoAsientoCentro;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * Repositorio de los archivos XML contables de Centroamerica.
 */
@Repository
public interface ArchivoAsientoCentroRepository
        extends JpaRepository<ArchivoAsientoCentro, Integer> {

    /**
     * Consulta los archivos generados mas recientes.
     *
     * @return archivos ordenados del mas reciente al mas antiguo.
     */
    @Query(
            value = "SELECT TOP 50 * "
                    + "FROM dbo.archivoAsientoCentro "
                    + "ORDER BY fechaproceso DESC, id DESC",
            nativeQuery = true)
    List<ArchivoAsientoCentro> findLatest();
}
