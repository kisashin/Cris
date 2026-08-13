package co.com.bnpparibas.cardif.closingclaims.domain.entity;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;

import java.io.*;
import java.util.Date;

import static org.junit.jupiter.api.Assertions.*;

class ArchivoCargueTBLTest {

    /** Helper que crea un {@link FileLoadId} con valores de ejemplo. */
    private FileLoadId buildId() {
        return FileLoadId.builder()
                .nombre("archivo.xlsx")
                .fechaproceso(new Date())
                .build();
    }

    /** Helper que crea una instancia completa usando el *builder* generado por Lombok. */
    private ArchivoCargueTBL buildFullWithBuilder() {
        return ArchivoCargueTBL.builder()
                .id(buildId())
                .estado("PENDIENTE")
                .registros(100)
                .errores(2)
                .cargadosanterior(5)
                .porcargar(30)
                .idModulo(1)
                .build();
    }

    /* --------------------------------------------------------------- *
     *  Builder / Getters
     * --------------------------------------------------------------- */
    @Nested
    @DisplayName("Builder / Getters")
    class BuilderAndGetters {

        @Test
        @DisplayName("todos los campos se copian correctamente")
        void allFieldsAreSet() {
            ArchivoCargueTBL entity = buildFullWithBuilder();

            // Id compuesto
            assertNotNull(entity.getId());
            assertEquals("archivo.xlsx", entity.getId().getNombre());
            assertNotNull(entity.getId().getFechaproceso());

            // Campos simples
            assertEquals("PENDIENTE", entity.getEstado());
            assertEquals(100, entity.getRegistros());
            assertEquals(2, entity.getErrores());
            assertEquals(5, entity.getCargadosanterior());
            assertEquals(30, entity.getPorcargar());
            assertEquals(1, entity.getIdModulo());
        }
    }

    /* --------------------------------------------------------------- *
     *  No‑args constructor + Setters
     * --------------------------------------------------------------- */
    @Nested
    @DisplayName("No‑args constructor / Setters")
    class NoArgsAndSetters {

        @Test
        @DisplayName("puede crear la entidad y asignar valores mediante setters")
        void setAndGet() {
            ArchivoCargueTBL entity = new ArchivoCargueTBL();

            FileLoadId id = buildId();
            entity.setId(id);
            entity.setEstado("CARGADO");
            entity.setRegistros(50);
            entity.setErrores(0);
            entity.setCargadosanterior(10);
            entity.setPorcargar(100);
            entity.setIdModulo(1);

            assertEquals(id, entity.getId());
            assertEquals("CARGADO", entity.getEstado());
            assertEquals(50, entity.getRegistros());
            assertEquals(0, entity.getErrores());
            assertEquals(10, entity.getCargadosanterior());
            assertEquals(100, entity.getPorcargar());
            assertEquals(1, entity.getIdModulo());
        }
    }

    /* --------------------------------------------------------------- *
     *  All‑args constructor
     * --------------------------------------------------------------- */
    @Nested
    @DisplayName("All‑args constructor")
    class AllArgsConstructor {

        @Test
        @DisplayName("todos los campos pueden inicializarse mediante el constructor generado")
        void allArgs() {
            FileLoadId id = buildId();

            ArchivoCargueTBL entity = new ArchivoCargueTBL(
                    id,
                    "PROCESADO",
                    200,
                    3,
                    20,
                    80,
                    1
            );

            assertEquals(id, entity.getId());
            assertEquals("PROCESADO", entity.getEstado());
            assertEquals(200, entity.getRegistros());
            assertEquals(3, entity.getErrores());
            assertEquals(20, entity.getCargadosanterior());
            assertEquals(80, entity.getPorcargar());
            assertEquals(1, entity.getIdModulo());
        }
    }

    /* --------------------------------------------------------------- *
     *  Serialización
     * --------------------------------------------------------------- */
    @Nested
    @DisplayName("Serialización")
    class Serialization {

        @Test
        @DisplayName("puede serializarse y deserializarse manteniendo los valores")
        void serializeDeserialize() throws IOException, ClassNotFoundException {
            ArchivoCargueTBL original = buildFullWithBuilder();

            // ---------- Serializar ----------
            byte[] bytes;
            try (ByteArrayOutputStream bos = new ByteArrayOutputStream();
                 ObjectOutputStream out = new ObjectOutputStream(bos)) {
                out.writeObject(original);
                out.flush();
                bytes = bos.toByteArray();
            }

            // ---------- Deserializar ----------
            ArchivoCargueTBL deserialized;
            try (ByteArrayInputStream bis = new ByteArrayInputStream(bytes);
                 ObjectInputStream in = new ObjectInputStream(bis)) {
                deserialized = (ArchivoCargueTBL) in.readObject();
            }

            // ---------- Comparaciones campo a campo ----------
            assertNotNull(deserialized.getId());
            assertEquals(original.getId().getNombre(),
                    deserialized.getId().getNombre(),
                    "El nombre del archivo debe coincidir");
            assertEquals(original.getId().getFechaproceso(),
                    deserialized.getId().getFechaproceso(),
                    "La fecha de proceso debe coincidir");

            assertEquals(original.getEstado(), deserialized.getEstado());
            assertEquals(original.getRegistros(), deserialized.getRegistros());
            assertEquals(original.getErrores(), deserialized.getErrores());
            assertEquals(original.getCargadosanterior(), deserialized.getCargadosanterior());
            assertEquals(original.getPorcargar(), deserialized.getPorcargar());
            assertEquals(original.getIdModulo(), deserialized.getIdModulo());
        }
    }

    /* --------------------------------------------------------------- *
     *  Valores por defecto (constructor sin argumentos)
     * --------------------------------------------------------------- */
    @Nested
    @DisplayName("Valores por defecto")
    class DefaultValues {

        @Test
        @DisplayName("todos los campos son null al usar el constructor sin argumentos")
        void defaultsAreNull() {
            ArchivoCargueTBL entity = new ArchivoCargueTBL();

            assertNull(entity.getId());
            assertNull(entity.getEstado());
            assertNull(entity.getRegistros());
            assertNull(entity.getErrores());
            assertNull(entity.getCargadosanterior());
            assertNull(entity.getPorcargar());
            assertNull(entity.getIdModulo());
        }
    }
}
