ClaimAccountingControllerImpl

package co.com.bnpparibas.cardif.cierres.api.controller.impl;

import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Controller;

import co.com.bnpparibas.cardif.cierres.api.controller.ClaimAccountingController;
import co.com.bnpparibas.cardif.cierres.api.dtos.GenerateAccountingRequestDto;
import co.com.bnpparibas.cardif.cierres.api.dtos.LoadClaimRequestDto;
import co.com.bnpparibas.cardif.cierres.api.dtos.RegisterAccountingRequestDto;
import co.com.bnpparibas.cardif.cierres.api.dtos.SendAccountingRequestDto;
import co.com.bnpparibas.cardif.cierres.domain.service.ClaimAccountingService;
import co.com.bnpparibas.webservicemask.model.ws.response.BNPResponse;

import lombok.RequiredArgsConstructor;

@Controller
@RequiredArgsConstructor
public class ClaimAccountingControllerImpl implements ClaimAccountingController {

	private final ClaimAccountingService service;

	@Override
	public BNPResponse getAccountingDate() {
		return new BNPResponse(HttpStatus.OK, HttpStatus.OK.name(), service.getAccountingDate());
	}

	@Override
	public BNPResponse getProducts() {
		return new BNPResponse(HttpStatus.OK, HttpStatus.OK.name(), service.getProducts());
	}

	@Override
	public BNPResponse loadClaims(LoadClaimRequestDto request) {
		return new BNPResponse(HttpStatus.OK, HttpStatus.OK.name(), service.loadClaims(request));
	}

	@Override
	public BNPResponse generateEntry(GenerateAccountingRequestDto request) {
		return new BNPResponse(HttpStatus.OK, HttpStatus.OK.name(), service.generateEntry(request));
	}

	@Override
	public BNPResponse registerEntry(RegisterAccountingRequestDto request) {
		service.registerEntry(request);
		return new BNPResponse(HttpStatus.OK, HttpStatus.OK.name(), null);
	}

	@Override
	public BNPResponse totalByAccount(GenerateAccountingRequestDto request) {
		return new BNPResponse(HttpStatus.OK, HttpStatus.OK.name(), service.totalByAccount(request));
	}

	@Override
	public BNPResponse sendEntry(SendAccountingRequestDto request) {
		return new BNPResponse(HttpStatus.OK, HttpStatus.OK.name(), service.sendEntry(request));
	}

	@Override
	public BNPResponse ping() {
		return new BNPResponse(HttpStatus.OK, HttpStatus.OK.name(), "OK");
	}
}
