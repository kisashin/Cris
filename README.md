ClaimAccountingControllerImplTest

package co.com.bnpparibas.cardif.controller.impl;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.util.Collections;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.mockito.junit.jupiter.MockitoExtension;

import co.com.bnpparibas.cardif.builders.ClaimAccountingBuilder;
import co.com.bnpparibas.cardif.cierres.api.controller.impl.ClaimAccountingControllerImpl;
import co.com.bnpparibas.cardif.cierres.api.dtos.GenerateAccountingRequestDto;
import co.com.bnpparibas.cardif.cierres.domain.dtos.AccountingDateResponseDto;
import co.com.bnpparibas.cardif.cierres.domain.dtos.SendResponseDto;
import co.com.bnpparibas.cardif.cierres.domain.service.ClaimAccountingService;
import co.com.bnpparibas.webservicemask.model.ws.response.BNPResponse;

@ExtendWith(MockitoExtension.class)
class ClaimAccountingControllerImplTest {

	@InjectMocks
	private ClaimAccountingControllerImpl controller;

	@Mock
	private ClaimAccountingService service;

	@BeforeEach
	void setUp() {
		MockitoAnnotations.initMocks(this);
	}

	@Test
	void getAccountingDate_envuelveEnBNPResponse() {
		when(service.getAccountingDate()).thenReturn(new AccountingDateResponseDto("20240630"));

		BNPResponse response = controller.getAccountingDate();

		assertEquals(200, response.getReturnCode());
		AccountingDateResponseDto body = (AccountingDateResponseDto) response.getBodyResponse();
		assertEquals("20240630", body.getAccountingDate());
	}

	@Test
	void generateEntry_delegaAlServicio() {
		when(service.generateEntry(any(GenerateAccountingRequestDto.class)))
			.thenReturn(Collections.emptyList());

		BNPResponse response = controller.generateEntry(ClaimAccountingBuilder.generateRequest());

		assertEquals(200, response.getReturnCode());
		assertNotNull(response);
	}

	@Test
	void sendEntry_devuelveOk() {
		when(service.sendEntry(any())).thenReturn(new SendResponseDto("x.XML", "Interfaz enviada a contabilidad."));

		BNPResponse response = controller.sendEntry(ClaimAccountingBuilder.sendRequest());

		SendResponseDto body = (SendResponseDto) response.getBodyResponse();
		assertEquals("x.XML", body.getFileName());
		assertEquals(200, response.getReturnCode());
	}

	@Test
	void registerEntry_noRetornaBody() {
		BNPResponse response = controller.registerEntry(
			(co.com.bnpparibas.cardif.cierres.api.dtos.RegisterAccountingRequestDto)
			toRegister(ClaimAccountingBuilder.generateRequest()));

		verify(service).registerEntry(any());
		assertEquals(200, response.getReturnCode());
	}

	@Test
	void ping_ok() {
		BNPResponse response = controller.ping();
		assertEquals(200, response.getReturnCode());
	}

	private co.com.bnpparibas.cardif.cierres.api.dtos.RegisterAccountingRequestDto toRegister(
			GenerateAccountingRequestDto g) {
		co.com.bnpparibas.cardif.cierres.api.dtos.RegisterAccountingRequestDto r =
			new co.com.bnpparibas.cardif.cierres.api.dtos.RegisterAccountingRequestDto();
		r.setProduct(g.getProduct());
		r.setComment(g.getComment());
		return r;
	}
}
