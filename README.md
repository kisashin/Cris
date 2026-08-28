package co.com.bnpparibas.cardif.closingclaims.domain.dtos.cardifcenterclosing;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.function.Consumer;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

class AccountingXmlFileTest {

    private AccountingXmlFile file() {
        return AccountingXmlFile.builder()
                .movementType("Pago")
                .fileName("Sinie_ReasegCentro_Pago20260824.xml")
                .lineCount(4)
                .content("<SSC/>")
                .build();
    }

    @Test
    @DisplayName("El builder asigna todos los campos")
    void builderAssignsEveryField() {
        AccountingXmlFile result = file();

        assertEquals("Pago", result.getMovementType());
        assertEquals(
                "Sinie_ReasegCentro_Pago20260824.xml",
                result.getFileName());
        assertEquals(4, result.getLineCount());
        assertEquals("<SSC/>", result.getContent());
    }

    @Test
    @DisplayName("Los setters asignan todos los campos")
    void settersAssignEveryField() {
        AccountingXmlFile result = new AccountingXmlFile();

        assertNull(result.getMovementType());
        assertEquals(0, result.getLineCount());

        result.setMovementType("Constitucion");
        result.setFileName("archivo.xml");
        result.setLineCount(7);
        result.setContent("<SSC/>");

        assertEquals("Constitucion", result.getMovementType());
        assertEquals("archivo.xml", result.getFileName());
        assertEquals(7, result.getLineCount());
        assertEquals("<SSC/>", result.getContent());
    }

    @Test
    @DisplayName("El constructor con todos los argumentos asigna los campos")
    void allArgsConstructor() {
        AccountingXmlFile result = new AccountingXmlFile(
                "RevPago", "f.xml", 1, "<SSC/>");

        assertNotNull(result);
        assertEquals("RevPago", result.getMovementType());
        assertEquals(1, result.getLineCount());
    }

    @Test
    @DisplayName("equals, hashCode y toString reflejan el contenido")
    void equalsHashCodeAndToString() {
        AccountingXmlFile first = file();
        AccountingXmlFile second = file();

        assertEquals(first, second);
        assertEquals(first, first);
        assertEquals(first.hashCode(), second.hashCode());
        assertNotEquals(first, null);
        assertNotEquals(first, "otro tipo");
        assertNotEquals(first, new AccountingXmlFile());
        assertTrue(first.toString().contains("Pago"));
    }

    @Test
    @DisplayName("equals detecta diferencias en cualquier campo")
    void equalsDetectsEveryFieldDifference() {
        assertNotEquals(file(), modified(f -> f.setMovementType("X")));
        assertNotEquals(file(), modified(f -> f.setFileName("X")));
        assertNotEquals(file(), modified(f -> f.setLineCount(99)));
        assertNotEquals(file(), modified(f -> f.setContent("X")));
    }

    @Test
    @DisplayName("equals compara correctamente los campos nulos")
    void equalsHandlesNullFields() {
        AccountingXmlFile empty = new AccountingXmlFile();
        AccountingXmlFile other = new AccountingXmlFile();

        assertEquals(empty, other);
        assertEquals(empty.hashCode(), other.hashCode());

        other.setMovementType("Pago");
        assertNotEquals(empty, other);
        assertNotEquals(other, empty);
        assertNotNull(empty.toString());
    }

    private AccountingXmlFile modified(Consumer<AccountingXmlFile> change) {
        AccountingXmlFile result = file();
        change.accept(result);
        return result;
    }
}
