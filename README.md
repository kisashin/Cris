package co.com.bnpparibas.cardif.closingclaims.infraestructure.repository;

import co.com.bnpparibas.cardif.closingclaims.domain.entity.ArchivoAsientoCardifXml;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ArchivoAsientoCardifXmlRepository
        extends JpaRepository<ArchivoAsientoCardifXml, Integer> {

    @Query(
            value = "SELECT TOP 50 * "
                    + "FROM dbo.archivoAsientoCardifXml "
                    + "ORDER BY fechaproceso DESC, id DESC",
            nativeQuery = true)
    List<ArchivoAsientoCardifXml> findLatest();

    @Modifying(clearAutomatically = true, flushAutomatically = true)
    @Query(
            value = "DELETE FROM dbo.archivoAsientoCardifXml",
            nativeQuery = true)
    int deleteAllFiles();
}
