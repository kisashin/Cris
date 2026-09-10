package co.com.bnpparibas.cardif.closingclaims.infraestructure.repository;

import co.com.bnpparibas.cardif.closingclaims.domain.entity.ArchivoReporteAvalExcel;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ArchivoReporteAvalExcelRepository
        extends JpaRepository<ArchivoReporteAvalExcel, Integer> {

    @Query(
            value = "SELECT TOP 1 * "
                    + "FROM dbo.archivoReporteAvalExcel "
                    + "ORDER BY fechaproceso DESC, id DESC",
            nativeQuery = true)
    List<ArchivoReporteAvalExcel> findLatest();

    @Modifying(clearAutomatically = true, flushAutomatically = true)
    @Query(
            value = "DELETE FROM dbo.archivoReporteAvalExcel",
            nativeQuery = true)
    int deleteAllFiles();
}
