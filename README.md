ClaimAccountingServiceImpl

package co.com.bnpparibas.cardif.cierres.domain.service.impl;

import java.util.List;
import java.util.concurrent.locks.ReentrantLock;
import java.util.stream.Collectors;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import co.com.bnpparibas.cardif.cierres.api.dtos.GenerateAccountingRequestDto;
import co.com.bnpparibas.cardif.cierres.api.dtos.LoadClaimRequestDto;
import co.com.bnpparibas.cardif.cierres.api.dtos.RegisterAccountingRequestDto;
import co.com.bnpparibas.cardif.cierres.api.dtos.SendAccountingRequestDto;
import co.com.bnpparibas.cardif.cierres.domain.dtos.AccountTotalRowDto;
import co.com.bnpparibas.cardif.cierres.domain.dtos.AccountingDateResponseDto;
import co.com.bnpparibas.cardif.cierres.domain.dtos.AccountingEntryRowDto;
import co.com.bnpparibas.cardif.cierres.domain.dtos.LoadMessageResponseDto;
import co.com.bnpparibas.cardif.cierres.domain.dtos.ProductResponseDto;
import co.com.bnpparibas.cardif.cierres.domain.dtos.SendResponseDto;
import co.com.bnpparibas.cardif.cierres.domain.service.ClaimAccountingService;
import co.com.bnpparibas.cardif.cierres.infraestructure.repository.ClaimAccountingRepository;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Service
@Slf4j
@RequiredArgsConstructor
public class ClaimAccountingServiceImpl implements ClaimAccountingService {

    /** Emitidos juntos por el botón Enviar del legacy. "Reaseguro" es el nombre del menú, no el alcance. */
    private static final String[] JOURNAL_TYPES = { "SINIE", "LRVSI", "CRVSI" };

    /**
     * Serializa el envío. sp_XMLAsientosPru usa la temp global ##sp_HistoricoAsientosPru
     * y la tabla dbo._##XML_Asiento (truncate+insert): dos envíos simultáneos se
     * corromperían el XML entre sí. Es contabilidad, así que se serializa a nivel app.
     * (Si mañana esto corre en más de una instancia, este lock NO basta: haría falta
     *  un lock distribuido o sp_getapplock en BD. Anotado.)
     */
    private static final ReentrantLock SEND_LOCK = new ReentrantLock();

    private final ClaimAccountingRepository repository;

    // ---------------- lecturas ----------------

    @Override
    public AccountingDateResponseDto getAccountingDate() {
        return new AccountingDateResponseDto(repository.getAccountingDate());
    }

    @Override
    public List<ProductResponseDto> getProducts() {
        return repository.getProducts().stream()
                .map(ProductResponseDto::new)
                .collect(Collectors.toList());
    }

    // ---------------- cargar ----------------

    @Override
    public LoadMessageResponseDto loadClaims(LoadClaimRequestDto request) {
        boolean alpha = repository.countProductLayout(request.getProduct()) > 0; // layout=1 => Alfa
        String message = repository.loadClaims(request.getProduct(), alpha);
        return new LoadMessageResponseDto(message);
    }

    // ---------------- generar / total / registrar ----------------

    @Override
    public List<AccountingEntryRowDto> generateEntry(GenerateAccountingRequestDto request) {
        return repository.generateEntry(request.getComment(), request.getProduct());
    }

    @Override
    public List<AccountTotalRowDto> totalByAccount(GenerateAccountingRequestDto request) {
        return repository.totalByAccount(request.getComment(), request.getProduct());
    }

    @Override
    public void registerEntry(RegisterAccountingRequestDto request) {
        repository.registerEntry(request.getComment(), request.getProduct());
    }

    // ---------------- enviar (el corazón) ----------------

    @Override
    @Transactional("transactionManager")
    public SendResponseDto sendEntry(SendAccountingRequestDto request) {
        SEND_LOCK.lock();
        try {
            String period = buildPeriod();                 // YYYY/0MM
            String product = request.getProduct();
            String comment = request.getComment();
            String userName = resolveUserName(request);     // TODO SAML (ver abajo)

            String lastXmlName = null;
            for (String type : JOURNAL_TYPES) {
                String xml = repository.generateXml(type, period, product, comment);
                if (xml == null || xml.isEmpty()) {
                    continue; // el SP devolvió '0': no hay asientos de ese tipo, se salta
                }
                String xmlName = buildXmlName(comment, type, product, period);
                deliverToStcp(xmlName, xml); // entrega controlada desde Spring, NO el bcp del SP
                lastXmlName = xmlName;
            }

            if (lastXmlName == null) {
                return new SendResponseDto(null, "No se generaron asientos para enviar.");
            }

            // correo de notificación (ListaArhivos id=6). El @body original era la tabla HTML del grid.
            repository.notifyByMail(lastXmlName, userName, buildMailBody());

            // marca ha.estado = 'XML Generado' (modo 4)
            repository.markXmlGenerated(comment, product);

            return new SendResponseDto(lastXmlName, "Interfaz enviada a contabilidad.");
        } finally {
            SEND_LOCK.unlock();
        }
    }

    // ================= helpers =================

    /**
     * Periodo canónico YYYY/0MM (ej. 2024/007), el mismo que arma el legacy con
     * substring(1,4)+'/0'+substring(6,2). Si va mal (YYYY/MM sin el cero, o YYYYMM),
     * el WHERE de sp_XMLAsientosPru no matchea NADA y el XML sale vacío SIN error:
     * fallo silencioso idéntico al de Onbase. -> Blindar con test.
     */
    private String buildPeriod() {
        String raw = repository.getAccountingPeriodRaw(); // YYYY/MM/DD
        String year = raw.substring(0, 4);
        String month = raw.substring(5, 7);
        return year + "/0" + month;
    }

    /**
     * Réplica de sp_XMLAsientosPru:
     *   left(rtrim(ltrim(ajuste)),20) + tipo + '_' + prod + replace(periodo,'/0','') + '.XML'
     * con prod sin el cero a la izquierda, y espacios -> '_'.
     */
    private String buildXmlName(String comment, String type, String product, String period) {
        String prefix = comment == null ? "" : comment.trim();
        if (prefix.length() > 20) {
            prefix = prefix.substring(0, 20);
        }
        String prod = (product == null) ? ""
                : (product.startsWith("0") ? product.substring(1) : product);
        String name = prefix + type + "_" + prod + period.replace("/0", "") + ".XML";
        return name.replace(" ", "_");
    }

    // ---- SEAMS pendientes (bloqueados por info que aún no tenemos) ----

    /**
     * TODO STCP: entregar el XML al fichero/carpeta que lee la ETL. La ruta, el nombre
     * exacto y el disparo del JOB se confirman en la prueba de dev de mañana. Este es el
     * punto donde el módulo se puede caer en silencio (patrón Onbase): capturar ahí
     * ruta que lee la ETL + marca/columna que dispara el job + formato de archivo.
     */
    private void deliverToStcp(String xmlName, String xml) {
        log.info("TODO STCP: entregar {} ({} chars) a la ruta que lee la ETL", xmlName, xml.length());
        // throw new UnsupportedOperationException("Definir entrega STCP tras prueba dev");
    }

    /**
     * TODO SAML: el usuario NO debe venir del front (el legacy usaba My.User.Name).
     * Falta el resolutor de usuario autenticado de la casa (era la Tanda B que no llegó).
     */
    private String resolveUserName(SendAccountingRequestDto request) {
        return request.getUserName(); // provisional hasta cablear SAML
    }

    /**
     * TODO body: el legacy armaba una tabla HTML desde el GridView (función html()).
     * Con la grilla ahora en el front, este cuerpo hay que reconstruirlo server-side
     * o recibir el HTML ya armado. Placeholder para no bloquear.
     */
    private String buildMailBody() {
        return "Asiento de siniestros generado.";
    }
}
