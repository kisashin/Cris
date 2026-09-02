package co.com.bnpparibas.cardif.cierres.domain.util.helpers;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.Charset;
import java.util.ArrayList;
import java.util.List;

import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVParser;
import org.apache.commons.csv.CSVRecord;
import org.springframework.stereotype.Component;
import org.springframework.web.multipart.MultipartFile;

import co.com.bnpparibas.cardif.cierres.domain.util.constants.ExceptionConstants;
import co.com.bnpparibas.cardif.cierres.domain.util.exception.DataException;

@Component
public class ClaimFileHelper {

    public static final int COLUMNS = 46;

    private static final Charset ENCODING = Charset.forName("windows-1252");
    private static final char DELIMITER = ';';
    private static final String HEADER_FIRST_VALUE = "NORAMO";
    private static final String HEADER_SECOND_VALUE = "RAMO";

    private int incomplete;

    public List<String[]> read(MultipartFile file) {
        List<String[]> rows = new ArrayList<>();

        incomplete = 0;

        CSVFormat format = CSVFormat.DEFAULT
                .withDelimiter(DELIMITER)
                .withIgnoreEmptyLines(true)
                .withTrim(false);

        try (BufferedReader reader = new BufferedReader(
                new InputStreamReader(file.getInputStream(), ENCODING));
             CSVParser parser = new CSVParser(reader, format)) {

            boolean first = true;

            for (CSVRecord record : parser) {
                if (first) {
                    first = false;
                    if (isHeader(record)) {
                        continue;
                    }
                }

                if (record.size() < COLUMNS) {
                    incomplete++;
                }

                rows.add(toRow(record));
            }
        } catch (IOException e) {
            throw new DataException(ExceptionConstants.FILE_READ_ERROR, e);
        }

        if (rows.isEmpty()) {
            throw new DataException(ExceptionConstants.FILE_WITHOUT_RECORDS);
        }

        return rows;
    }

    /**
     * Filas que no traian las 46 columnas esperadas. Solo tiene valor despues
     * de leer el archivo.
     */
    public int countIncomplete(List<String[]> rows) {
        return incomplete;
    }

    private boolean isHeader(CSVRecord record) {
        if (record.size() == 0) {
            return false;
        }

        String value = record.get(0) == null ? "" : record.get(0).trim().toUpperCase();

        return HEADER_FIRST_VALUE.equals(value) || HEADER_SECOND_VALUE.equals(value);
    }

    private String[] toRow(CSVRecord record) {
        String[] row = new String[COLUMNS];

        for (int i = 0; i < COLUMNS && i < record.size(); i++) {
            String value = record.get(i);
            row[i] = value == null || value.isEmpty() ? null : value;
        }

        return row;
    }
}
