package co.com.bnpparibas.cardif.closingclaims.infraestructure.repository;

import co.com.bnpparibas.cardif.closingclaims.domain.entity.ArchivoAsientoCentro;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
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
     * Consulta los archivos generados mas recientes sin traer el contenido.
     *
     * @return archivos ordenados del mas reciente al mas antiguo.
     */
    @Query(
            value = "SELECT TOP 50 id, idLote, periodo, tipoMovimiento, "
                    + "nombreArchivo, NULL AS contenido, cantidadLineas, "
                    + "fechaproceso, estado "
                    + "FROM dbo.archivoAsientoCentro "
                    + "ORDER BY fechaproceso DESC, id DESC",
            nativeQuery = true)
    List<ArchivoAsientoCentro> findLatest();

    // NUEVO
    /**
     * Elimina todos los archivos generados previamente.
     *
     * @return cantidad de registros eliminados.
     */
    @Modifying(clearAutomatically = true, flushAutomatically = true)
    @Query(
            value = "DELETE FROM dbo.archivoAsientoCentro",
            nativeQuery = true)
    int deleteAllFiles();
}
