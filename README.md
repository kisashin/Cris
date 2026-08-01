updateReports(dateFrom: string | null, dateUntil: string | null, countryCode?: String): Observable<INewGeneralResponse<string>> {
    const headers = new HttpHeaders()
      .set('correlation_id', crypto.randomUUID())
      .set('request_id', crypto.randomUUID())
      .set('_p', countryCode?.trim() || crypto.randomUUID())
      .set('Content-Type', 'application/json')
      .set('Accept', 'text/plain');

    const body = { dateFrom: dateFrom ?? null, dateUntil: dateUntil ?? null };

    return this.http.post<string>(
      `${this.baseUrl}/v1/update-partner-report`,
      body,
      {
        headers,
        responseType: 'text' as 'json'
      }
    ).pipe(
      map((txt: string) => ({
        bodyResponse: txt
      }) as INewGeneralResponse<string>)
    );
  }

  .updateReports(
        null,
        null,
        this.uploadFlag
      )


@Modifying
    @Transactional
    @Query(value =
            "UPDATE dbo.tbl_Archivo_socios " +
                    "SET nombredatos = NULL, " +
                    "    nombremov = NULL, " +
                    "    fechaproceso = GETDATE(), " +
                    "    estado = 'PENDIENTE'",
            nativeQuery = true)
    int markAsPending();



package co.com.bnpparibas.cardif.closingclaims.infraestructure.repository;

import co.com.bnpparibas.cardif.closingclaims.domain.entity.CentralAmericaPartnerReport;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;

@Repository
public interface CentralAmericaPartnerReportRepository
        extends JpaRepository<CentralAmericaPartnerReport, Integer> {

    @Query(value =
            "SELECT " +
                    "id, " +
                    "nombredatos, " +
                    "nombremov, " +
                    "fechaproceso, " +
                    "estado " +
                    "FROM dbo.tbl_Archivo_socios",
            nativeQuery = true)
    List<CentralAmericaPartnerReport> findAllReports();

    @Modifying
    @Transactional
    @Query(value =
            "UPDATE dbo.tbl_Archivo_socios " +
                    "SET nombredatos = NULL, " +
                    "    nombremov = NULL, " +
                    "    fechaproceso = GETDATE(), " +
                    "    estado = 'PENDIENTE'",
            nativeQuery = true)
    int markAsPending();

}    
