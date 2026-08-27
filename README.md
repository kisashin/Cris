package co.com.bnpparibas.cardif.closingclaims.infraestructure.repository;

import co.com.bnpparibas.cardif.closingclaims.domain.entity.ArchivoAsientoAvalXml;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ArchivoAsientoAvalXmlRepository
        extends JpaRepository<ArchivoAsientoAvalXml, Integer> {

    @Query(
            value = "SELECT TOP 50 * "
                    + "FROM dbo.archivoAsientoAvalXml "
                    + "ORDER BY fechaproceso DESC, id DESC",
            nativeQuery = true)
    List<ArchivoAsientoAvalXml> findLatest();

    @Modifying(clearAutomatically = true, flushAutomatically = true)
    @Query(
            value = "DELETE FROM dbo.archivoAsientoAvalXml",
            nativeQuery = true)
    int deleteAllFiles();
}
