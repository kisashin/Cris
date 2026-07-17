ClaimAccountingRepositoryImplTest

package co.com.bnpparibas.cardif.repository.imp;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyInt;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.when;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;

import javax.persistence.EntityManager;
import javax.persistence.Query;
import javax.persistence.StoredProcedureQuery;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.mockito.junit.jupiter.MockitoExtension;

import co.com.bnpparibas.cardif.builders.ClaimAccountingBuilder;
import co.com.bnpparibas.cardif.cierres.domain.dtos.AccountingEntryRowDto;
import co.com.bnpparibas.cardif.cierres.infraestructure.repository.impl.ClaimAccountingRepositoryImpl;

@ExtendWith(MockitoExtension.class)
class ClaimAccountingRepositoryImplTest {

	@InjectMocks
	private ClaimAccountingRepositoryImpl repository;

	@Mock
	private EntityManager entityManager;

	@Mock
	private StoredProcedureQuery storedProcedureQuery;

	@Mock
	private Query nativeQuery;

	@BeforeEach
	void setUp() {
		MockitoAnnotations.initMocks(this);
	}

	/**
	 * El test que importa: valida que las 27 columnas del modo 1 se mapean en el
	 * orden correcto. Si alguien reordena el SELECT del SP, este test se cae ANTES
	 * de que el error llegue a contabilidad como XML mal armado.
	 */
	@Test
	void generateEntry_mapeaLas27ColumnasEnOrden() {
		when(entityManager.createStoredProcedureQuery(anyString())).thenReturn(storedProcedureQuery);
		when(storedProcedureQuery.getResultList())
			.thenReturn(Collections.singletonList(ClaimAccountingBuilder.entryRowMode1()));

		List<AccountingEntryRowDto> rows =
			repository.generateEntry(ClaimAccountingBuilder.COMMENT, ClaimAccountingBuilder.PRODUCT);

		assertEquals(1, rows.size());
		AccountingEntryRowDto r = rows.get(0);
		assertEquals("SINIE", r.getJournalType());
		assertEquals("51144000", r.getAccountCode());
		assertEquals("Avisos", r.getTransactionReference());
		assertEquals("D", r.getDebitCredit());
		assertEquals("0430", r.getProduct());
		assertEquals("SIN-001", r.getClaimNumber());          // última posición (col 27)
		assertEquals(0, r.getTransactionAmount().compareTo(new java.math.BigDecimal("150000")));
	}

	@Test
	@SuppressWarnings("unchecked")
	void getProducts_devuelveLista() {
		when(entityManager.createNativeQuery(anyString())).thenReturn(nativeQuery);
		when(nativeQuery.getResultList()).thenReturn(Arrays.asList("2005", "3601"));

		List<String> products = repository.getProducts();

		assertEquals(2, products.size());
		assertTrue(products.contains("2005"));
	}

	@Test
	void generateXml_traduceCeroAVacio() {
		when(entityManager.createStoredProcedureQuery(anyString())).thenReturn(storedProcedureQuery);
		when(storedProcedureQuery.getResultList()).thenReturn(Collections.singletonList("0"));

		String xml = repository.generateXml("SINIE", "2024/006", "2005", ClaimAccountingBuilder.COMMENT);

		assertEquals("", xml); // '0' del SP => sin asientos => cadena vacía
	}

	@Test
	void generateXml_devuelveElXml() {
		String payload = "<?xml version=\"1.0\" encoding=\"UTF-8\" ?><SSC/>";
		when(entityManager.createStoredProcedureQuery(anyString())).thenReturn(storedProcedureQuery);
		when(storedProcedureQuery.getResultList()).thenReturn(Collections.singletonList(payload));

		String xml = repository.generateXml("LRVSI", "2024/006", "2005", ClaimAccountingBuilder.COMMENT);

		assertEquals(payload, xml);
	}
}
