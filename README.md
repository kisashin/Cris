package co.com.bnpparibas.cardif.closingclaims.infraestructure.repository;

import co.com.bnpparibas.cardif.closingclaims.domain.entity.ClaimMovementHistory;
import co.com.bnpparibas.cardif.closingclaims.domain.util.anums.NewsStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ClaimMovementHistoryRepository
        extends JpaRepository<ClaimMovementHistory, Long> {

    @Query("SELECT m FROM ClaimMovementHistory m "
            + "WHERE m.numeroSiniestro = :claimNumber "
            + "AND NOT EXISTS (SELECT 1 FROM IndividualNewsHistory n "
            + "WHERE n.idCarvajal = m.idCarvajal AND n.estado = :status)")
    List<ClaimMovementHistory> findAvailableByClaimNumber(
            @Param("claimNumber") String claimNumber,
            @Param("status") NewsStatus status);
}