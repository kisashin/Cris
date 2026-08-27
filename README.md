package co.com.bnpparibas.cardif.closingclaims.domain.util.helpers;

import co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia.ColombiaAccountingLine;
import co.com.bnpparibas.cardif.closingclaims.domain.dtos.closingcolombia.ColombiaXmlFile;
import org.springframework.stereotype.Component;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Arma los archivos XML contables de Colombia a partir de las lineas
 * devueltas por los procedimientos almacenados.
 */
@Component
public class ColombiaAccountingXmlHelper {

    private static final String DIRECT_FAMILY = "Directas";

    private static final String HEADER =
            "<?xml version=\"1.0\" encoding=\"UTF-8\" ?><SSC>"
                    + "<SunSystemsContext><BusinessUnit>S01</BusinessUnit>"
                    + "<BudgetCode>A</BudgetCode></SunSystemsContext>"
                    + "<Payload><Ledger>";

    private static final String FOOTER = "</Ledger></Payload></SSC>";

    private static final String LINE_TAG = "<Line>";
    private static final String FILE_EXTENSION = ".xml";
    private static final String REVERSAL_PREFIX = "rv";
    private static final String KEY_SEPARATOR = "|";

    private static final DateTimeFormatter FILE_DATE_FORMAT =
            DateTimeFormatter.ofPattern("yyyyMMdd");

    private static final Map<String, String> FILE_PREFIXES =
            buildFilePrefixes();

    private static final List<String> MOVEMENT_ORDER = Arrays.asList(
            "Constitucion", "Liberacion", "Objecion", "Pago", "RevPago");

    public List<ColombiaXmlFile> buildFiles(
            List<ColombiaAccountingLine> lines) {

        List<ColombiaXmlFile> files = new ArrayList<>();

        if (lines == null || lines.isEmpty()) {
            return files;
        }

        String fileDate = LocalDate.now().format(FILE_DATE_FORMAT);
        Map<String, List<ColombiaAccountingLine>> groups = groupLines(lines);

        for (Map.Entry<String, List<ColombiaAccountingLine>> entry
                : groups.entrySet()) {

            ColombiaAccountingLine reference = entry.getValue().get(0);

            if (DIRECT_FAMILY.equals(reference.getFamily())) {
                files.add(buildDirectFile(reference));
            } else {
                files.add(buildGroupedFile(
                        reference, entry.getValue(), fileDate));
            }
        }

        files.sort((first, second) -> {
            int familyComparison = first.getFamily()
                    .compareTo(second.getFamily());

            return familyComparison != 0
                    ? familyComparison
                    : Integer.compare(
                    movementOrder(first.getMovementType()),
                    movementOrder(second.getMovementType()));
        });

        return files;
    }

    private Map<String, List<ColombiaAccountingLine>> groupLines(
            List<ColombiaAccountingLine> lines) {

        Map<String, List<ColombiaAccountingLine>> groups =
                new LinkedHashMap<>();

        for (ColombiaAccountingLine line : lines) {
            if (line.getContent() == null) {
                continue;
            }

            groups.computeIfAbsent(buildKey(line), key -> new ArrayList<>())
                    .add(line);
        }

        return groups;
    }

    private String buildKey(ColombiaAccountingLine line) {
        if (DIRECT_FAMILY.equals(line.getFamily())) {
            return line.getFamily() + KEY_SEPARATOR
                    + line.getPass() + KEY_SEPARATOR
                    + line.getFileName();
        }

        return line.getFamily() + KEY_SEPARATOR
                + line.getPass() + KEY_SEPARATOR
                + line.getMovementType();
    }

    private ColombiaXmlFile buildDirectFile(
            ColombiaAccountingLine line) {

        return ColombiaXmlFile.builder()
                .family(line.getFamily())
                .period(line.getPeriod())
                .movementType(line.getMovementType())
                .fileName(line.getFileName())
                .lineCount(countLines(line.getContent()))
                .content(line.getContent())
                .build();
    }

    private ColombiaXmlFile buildGroupedFile(
            ColombiaAccountingLine reference,
            List<ColombiaAccountingLine> lines,
            String fileDate) {

        StringBuilder content = new StringBuilder(HEADER);
        lines.forEach(line -> content.append(line.getContent()));
        content.append(FOOTER);

        return ColombiaXmlFile.builder()
                .family(reference.getFamily())
                .period(reference.getPeriod())
                .movementType(reference.getMovementType())
                .fileName(buildFileName(reference, fileDate))
                .lineCount(lines.size())
                .content(content.toString())
                .build();
    }

    private String buildFileName(
            ColombiaAccountingLine reference,
            String fileDate) {

        String prefix = FILE_PREFIXES.getOrDefault(
                reference.getFamily(), reference.getFamily());

        String reversal = isReversal(reference) ? REVERSAL_PREFIX : "";

        return reversal + prefix + reference.getMovementType()
                + fileDate + FILE_EXTENSION;
    }

    private boolean isReversal(ColombiaAccountingLine line) {
        return line.getPass() != null && line.getPass() == 2;
    }

    private int countLines(String content) {
        int count = 0;
        int index = content.indexOf(LINE_TAG);

        while (index >= 0) {
            count++;
            index = content.indexOf(LINE_TAG, index + LINE_TAG.length());
        }

        return count;
    }

    private int movementOrder(String movementType) {
        int index = MOVEMENT_ORDER.indexOf(movementType);
        return index < 0 ? MOVEMENT_ORDER.size() : index;
    }

    private static Map<String, String> buildFilePrefixes() {
        Map<String, String> prefixes = new HashMap<>();
        prefixes.put("ReasegAlfa", "ReasegAlf_Hogar");
        prefixes.put("ReasegCardif", "ReasegDirectas");
        prefixes.put("CoaseguroCedido", "CoasegCed_");
        prefixes.put("ReasegCedidoHogar", "ReasegCed_Hogar");
        return prefixes;
    }
}
