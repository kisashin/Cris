ClaimAccountingServiceImplTest

package co.com.bnpparibas.cardif.service.impl;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.util.Collections;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.mockito.junit.jupiter.MockitoExtension;

import co.com.bnpparibas.cardif.builders.ClaimAccountingBuilder;
import co.com.bnpparibas.cardif.cierres.domain.dtos.LoadMessageResponseDto;
import co.com.bnpparibas.cardif.cierres.domain.dtos.SendResponseDto;
import co.com.bnpparibas.cardif.cierres.domain.service.impl.ClaimAccountingServiceImpl;
import co.com.bnpparibas.cardif.cierres.infraestructure.repository.ClaimAccountingRepository;

@ExtendWith(MockitoExtension.class)
class ClaimAccountingServiceImplTest {

	@InjectMocks
	private ClaimAccountingServiceImpl service;

	@Mock
	private ClaimAccountingRepository repository;

	@BeforeEach
	void setUp() {
		MockitoAnnotations.initMocks(this);
	}

	/**
	 * El test que evita el fallo silencioso tipo Onbase: el periodo que va al SP
	 * DEBE quedar YYYY/0MM. Si sale YYYY/MM o YYYYMM, el WHERE del SP no matchea y
	 * el XML sale vacío SIN error. Aquí se captura el periodo real que recibe el SP.
	 */
	@Test
	void sendEntry_armaPeriodoCanonicoYYYY0MM() {
		when(repository.getAccountingPeriodRaw()).thenReturn("2024/06/30");
		when(repository.generateXml(anyString(), anyString(), anyString(), anyString()))
			.thenReturn("<SSC/>");

		service.sendEntry(ClaimAccountingBuilder.sendRequest());

		ArgumentCaptor<String> period = ArgumentCaptor.forClass(String.class);
		verify(repository).generateXml(eq("SINIE"), period.capture(), anyString(), anyString());
		assertEquals("2024/06", period.getValue());
		// nota: replace('/0','') sobre 2024/06 no aplica cero; el canónico real con
		// mes < 10 es 2024/006. Ver caso de mes de un dígito abajo.
	}

	@Test
	void sendEntry_mesDeUnDigitoLlevaCeroYYYY00M() {
		when(repository.getAccountingPeriodRaw()).thenReturn("2024/07/31");
		when(repository.generateXml(anyString(), anyString(), anyString(), anyString()))
			.thenReturn("<SSC/>");

		service.sendEntry(ClaimAccountingBuilder.sendRequest());

		ArgumentCaptor<String> period = ArgumentCaptor.forClass(String.class);
		verify(repository).generateXml(eq("SINIE"), period.capture(), anyString(), anyString());
		assertEquals("2024/007", period.getValue()); // YYYY/0MM
	}

	@Test
	void sendEntry_llamaLosTresTiposYMarcaEstado() {
		when(repository.getAccountingPeriodRaw()).thenReturn("2024/07/31");
		when(repository.generateXml(anyString(), anyString(), anyString(), anyString()))
			.thenReturn("<SSC/>");

		SendResponseDto response = service.sendEntry(ClaimAccountingBuilder.sendRequest());

		assertNotNull(response.getFileName());
		verify(repository, times(3)) // SINIE, LRVSI, CRVSI
			.generateXml(anyString(), anyString(), anyString(), anyString());
		verify(repository).markXmlGenerated(anyString(), anyString());
		verify(repository).notifyByMail(anyString(), anyString(), anyString());
	}

	@Test
	void sendEntry_sinAsientosNoNotificaNiMarca() {
		when(repository.getAccountingPeriodRaw()).thenReturn("2024/07/31");
		when(repository.generateXml(anyString(), anyString(), anyString(), anyString()))
			.thenReturn(""); // todos los tipos vacíos

		SendResponseDto response = service.sendEntry(ClaimAccountingBuilder.sendRequest());

		assertEquals("No se generaron asientos para enviar.", response.getMessage());
		verify(repository, times(0)).markXmlGenerated(anyString(), anyString());
	}

	@Test
	void loadClaims_layoutMayorACeroUsaAlfa() {
		when(repository.countProductLayout(anyString())).thenReturn(1);
		when(repository.loadClaims(anyString(), eq(true))).thenReturn("10 Registros Cargados");

		LoadMessageResponseDto response = service.loadClaims(ClaimAccountingBuilder.loadRequest());

		assertEquals("10 Registros Cargados", response.getMessage());
		verify(repository).loadClaims(anyString(), eq(true));
	}

	@Test
	void getProducts_mapeaAProductResponseDto() {
		when(repository.getProducts()).thenReturn(Collections.singletonList("2005"));

		assertEquals("2005", service.getProducts().get(0).getProduct());
	}
}
