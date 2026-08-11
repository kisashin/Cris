package co.com.bnpparibas.cardif.closingclaims.infraestructure.repository;

import co.com.bnpparibas.cardif.closingclaims.domain.entity.IndividualNewsHistory;
import co.com.bnpparibas.cardif.closingclaims.domain.util.anums.NewsStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface IndividualNewsHistoryRepository
        extends JpaRepository<IndividualNewsHistory, Long> {

    List<IndividualNewsHistory> findByEstadoOrderByCodigoAsc(NewsStatus estado);

    Optional<IndividualNewsHistory> findByCodigoAndEstado(Long codigo, NewsStatus estado);

    boolean existsByIdCarvajalAndEstado(Long idCarvajal, NewsStatus estado);
}