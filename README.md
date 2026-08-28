package co.com.bnpparibas.cardif.closingclaims.domain.dtos.cardifcenterclosing;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.function.Consumer;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

class AccountingXmlLineTest {

    private AccountingXmlLine line() {
        return AccountingXmlLine.builder()
                .period("202608")
                .pass(1)
                .lineType(2)
                .movementType("Pago")
                .sequence(3L)
                .content("<Line/>")
                .build();
    }

    @Test
    @DisplayName("El builder asigna todos los campos")
    void builderAssignsEveryField() {
        AccountingXmlLine result = line();

        assertEquals("202608", result.getPeriod());
        assertEquals(1, result.getPass());
        assertEquals(2, result.getLineType());
        assertEquals("Pago", result.getMovementType());
        assertEquals(3L, result.getSequence());
        assertEquals("<Line/>", result.getContent());
    }

    @Test
    @DisplayName("Los setters asignan todos los campos")
    void settersAssignEveryField() {
        AccountingXmlLine result = new AccountingXmlLine();

        assertNull(result.getPeriod());

        result.setPeriod("202607");
        result.setPass(2);
        result.setLineType(0);
        result.setMovementType("Constitucion");
        result.setSequence(9L);
        result.setContent("<SSC/>");

        assertEquals("202607", result.getPeriod());
        assertEquals(2, result.getPass());
        assertEquals(0, result.getLineType());
        assertEquals("Constitucion", result.getMovementType());
        assertEquals(9L, result.getSequence());
        assertEquals("<SSC/>", result.getContent());
    }

    @Test
    @DisplayName("El constructor con todos los argumentos asigna los campos")
    void allArgsConstructor() {
        AccountingXmlLine result = new AccountingXmlLine(
                "202608", 1, 2, "Liberacion", 5L, "<Line/>");

        assertNotNull(result);
        assertEquals("Liberacion", result.getMovementType());
        assertEquals(5L, result.getSequence());
    }

    @Test
    @DisplayName("equals, hashCode y toString reflejan el contenido")
    void equalsHashCodeAndToString() {
        AccountingXmlLine first = line();
        AccountingXmlLine second = line();

        assertEquals(first, second);
        assertEquals(first, first);
        assertEquals(first.hashCode(), second.hashCode());
        assertNotEquals(first, null);
        assertNotEquals(first, "otro tipo");
        assertNotEquals(first, new AccountingXmlLine());
        assertTrue(first.toString().contains("202608"));
    }

    @Test
    @DisplayName("equals detecta diferencias en cualquier campo")
    void equalsDetectsEveryFieldDifference() {
        assertNotEquals(line(), modified(l -> l.setPeriod("202607")));
        assertNotEquals(line(), modified(l -> l.setPass(9)));
        assertNotEquals(line(), modified(l -> l.setLineType(9)));
        assertNotEquals(line(), modified(l -> l.setMovementType("X")));
        assertNotEquals(line(), modified(l -> l.setSequence(99L)));
        assertNotEquals(line(), modified(l -> l.setContent("X")));
    }

    @Test
    @DisplayName("equals compara correctamente los campos nulos")
    void equalsHandlesNullFields() {
        AccountingXmlLine empty = new AccountingXmlLine();
        AccountingXmlLine other = new AccountingXmlLine();

        assertEquals(empty, other);
        assertEquals(empty.hashCode(), other.hashCode());

        other.setPeriod("202608");
        assertNotEquals(empty, other);
        assertNotEquals(other, empty);
        assertNotNull(empty.toString());
    }

    private AccountingXmlLine modified(Consumer<AccountingXmlLine> change) {
        AccountingXmlLine result = line();
        change.accept(result);
        return result;
    }
}
