CardifPeruClosingTest

package co.com.bnpparibas.cardif.closingclaims.domain.entity;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.lang.reflect.Method;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

class CardifPeruClosingTest {

    @Test
    @DisplayName("Should create movement using builder")
    void shouldCreateMovementUsingBuilder() {
        CardifPeruClosing movement = CardifPeruClosing.builder()
                .idCarvajal(273767966630L)
                .partner("FINANCIERA TEST")
                .claimNumber("0672025A003012")
                .certificate("6722434176267121")
                .movementValue(95.0)
                .age(35)
                .currency("PEN")
                .build();

        assertNotNull(movement);
        assertEquals(273767966630L, movement.getIdCarvajal());
        assertEquals("FINANCIERA TEST", movement.getPartner());
        assertEquals("0672025A003012", movement.getClaimNumber());
        assertEquals("6722434176267121", movement.getCertificate());
        assertEquals(95.0, movement.getMovementValue());
        assertEquals(35, movement.getAge());
        assertEquals("PEN", movement.getCurrency());
    }

    @Test
    @DisplayName("Should cover all entity setters and getters")
    void shouldCoverAllEntitySettersAndGetters()
            throws ReflectiveOperationException {

        CardifPeruClosing movement = new CardifPeruClosing();
        int testedSetters = 0;

        for (Method setter : CardifPeruClosing.class.getMethods()) {
            if (isSetter(setter)) {
                Object expectedValue =
                        createTestValue(setter.getParameterTypes()[0]);

                setter.invoke(movement, expectedValue);

                String getterName = "get" + setter.getName().substring(3);
                Method getter =
                        CardifPeruClosing.class.getMethod(getterName);

                assertEquals(
                        expectedValue,
                        getter.invoke(movement),
                        setter.getName());

                testedSetters++;
            }
        }

        assertTrue(testedSetters > 60);
    }

    private boolean isSetter(Method method) {
        return method.getName().startsWith("set")
                && method.getParameterCount() == 1
                && method.getReturnType().equals(void.class);
    }

    private Object createTestValue(Class<?> fieldType) {
        if (String.class.equals(fieldType)) {
            return "test-value";
        }
        if (Long.class.equals(fieldType)) {
            return 1L;
        }
        if (Integer.class.equals(fieldType)) {
            return 1;
        }
        if (Double.class.equals(fieldType)) {
            return 100.0D;
        }
        throw new IllegalArgumentException(
                "Unsupported field type: " + fieldType.getName());
    }
}
