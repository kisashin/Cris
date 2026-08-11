package co.com.bnpparibas.cardif.closingclaims.domain.util.anums;

import co.com.bnpparibas.cardif.closingclaims.domain.util.messages.IndividualNewsMessage;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.EnumSource;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;

class IndividualNewsEnumsTest {

    @Test
    @DisplayName("NewsStatus declara los tres estados del flujo")
    void newsStatusDeclaresExpectedValues() {
        assertEquals(3, NewsStatus.values().length);
        assertEquals(NewsStatus.PENDIENTE, NewsStatus.valueOf("PENDIENTE"));
        assertEquals(NewsStatus.PROCESADO, NewsStatus.valueOf("PROCESADO"));
        assertEquals(NewsStatus.CANCELADO, NewsStatus.valueOf("CANCELADO"));
    }

    @Test
    @DisplayName("NewsType declara los dos tipos de novedad")
    void newsTypeDeclaresExpectedValues() {
        assertEquals(2, NewsType.values().length);
        assertEquals(NewsType.ACTUALIZA, NewsType.valueOf("ACTUALIZA"));
        assertEquals(NewsType.ELIMINA, NewsType.valueOf("ELIMINA"));
    }

    @ParameterizedTest
    @EnumSource(IndividualNewsMessage.class)
    @DisplayName("Cada mensaje controlado expone un texto no vacio")
    void individualNewsMessageExposesText(IndividualNewsMessage message) {
        assertNotNull(message.getMessage());
        assertFalse(message.getMessage().trim().isEmpty());
    }

    @Test
    @DisplayName("IndividualNewsMessage resuelve sus constantes por nombre")
    void individualNewsMessageResolvesByName() {
        assertEquals(IndividualNewsMessage.MOVEMENT_NOT_FOUND,
                IndividualNewsMessage.valueOf("MOVEMENT_NOT_FOUND"));
        assertEquals(5, IndividualNewsMessage.values().length);
    }
}