package co.com.bnpparibas.cardif.closingclaims.domain.util.helpers;

import co.com.bnpparibas.cardif.closingclaims.domain.dtos.cardifcenterclosing.AccountingXmlFileDTO;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.cardifcenterclosing.AccountingXmlLine;
import org.springframework.stereotype.Component;

import java.nio.charset.StandardCharsets;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Base64;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Arma los archivos XML contables a partir de las lineas devueltas por el
 * procedimiento almacenado.
 */
@Component
public class CardifCenterAccountingXmlHelper {

    private static final int HEADER_TYPE = 0;
    private static final int DETAIL_TYPE = 2;
    private static final int FOOTER_TYPE = 3;

    private static final String FILE_PREFIX = "Sinie_ReasegCentro_";
    private static final String FILE_EXTENSION = ".xml";

    private static final DateTimeFormatter FILE_DATE_FORMAT =
            DateTimeFormatter.ofPattern("yyyyMMdd");

    private static final List<String> MOVEMENT_ORDER = Arrays.asList(
            "Constitucion", "Liberacion", "Objecion", "Pago", "RevPago");

    /**
     * Construye un archivo por cada tipo de movimiento con lineas de detalle.
     *
     * @param lines lineas devueltas por el procedimiento.
     * @return archivos generados, con el contenido codificado en Base64.
     */
    public List<AccountingXmlFileDTO> buildFiles(
            List<AccountingXmlLine> lines) {

        List<AccountingXmlFileDTO> files = new ArrayList<>();

        if (lines == null || lines.isEmpty()) {
            return files;
        }

        String header = findEnvelope(lines, HEADER_TYPE);
        String footer = findEnvelope(lines, FOOTER_TYPE);
        String fileDate = LocalDate.now().format(FILE_DATE_FORMAT);

        for (Map.Entry<String, List<String>> entry
                : groupDetails(lines).entrySet()) {

            files.add(buildFile(
                    entry.getKey(),
                    entry.getValue(),
                    header,
                    footer,
                    fileDate));
        }

        files.sort((first, second) -> Integer.compare(
                movementOrder(first.getMovementType()),
                movementOrder(second.getMovementType())));

        return files;
    }

    private Map<String, List<String>> groupDetails(
            List<AccountingXmlLine> lines) {

        Map<String, List<String>> details = new LinkedHashMap<>();

        for (AccountingXmlLine line : lines) {
            if (isDetail(line)) {
                details.computeIfAbsent(
                                line.getMovementType(),
                                key -> new ArrayList<>())
                        .add(line.getContent());
            }
        }

        return details;
    }

    private AccountingXmlFileDTO buildFile(
            String movementType,
            List<String> details,
            String header,
            String footer,
            String fileDate) {

        StringBuilder content = new StringBuilder(header);
        details.forEach(content::append);
        content.append(footer);

        return AccountingXmlFileDTO.builder()
                .movementType(movementType)
                .fileName(FILE_PREFIX + movementType + fileDate
                        + FILE_EXTENSION)
                .lineCount(details.size())
                .content(Base64.getEncoder().encodeToString(
                        content.toString().getBytes(StandardCharsets.UTF_8)))
                .build();
    }

    private String findEnvelope(
            List<AccountingXmlLine> lines,
            int lineType) {

        return lines.stream()
                .filter(line -> line.getLineType() != null
                        && line.getLineType() == lineType)
                .map(AccountingXmlLine::getContent)
                .findFirst()
                .orElse("");
    }

    private boolean isDetail(AccountingXmlLine line) {
        return line.getLineType() != null
                && line.getLineType() == DETAIL_TYPE
                && line.getMovementType() != null
                && line.getContent() != null;
    }

    private int movementOrder(String movementType) {
        int index = MOVEMENT_ORDER.indexOf(movementType);
        return index < 0 ? MOVEMENT_ORDER.size() : index;
    }
}
