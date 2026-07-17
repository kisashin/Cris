ClaimAccountingController

package co.com.bnpparibas.cardif.cierres.api.controller;

import co.com.bnpparibas.cardif.cierres.api.dtos.GenerateAccountingRequestDto;
import co.com.bnpparibas.cardif.cierres.api.dtos.LoadClaimRequestDto;
import co.com.bnpparibas.cardif.cierres.api.dtos.RegisterAccountingRequestDto;
import co.com.bnpparibas.cardif.cierres.api.dtos.SendAccountingRequestDto;
import co.com.bnpparibas.webservicemask.model.ws.response.BNPResponse;
import co.com.bnpparibas.webservicemask.ws.template.BNPWebService;

import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

/**
 * Asientos Siniestros (reaseguro). Réplica de la pantalla legacy AsientosSiniestros.aspx.
 * El botón "Enviar" emite los 3 tipos de diario (SINIE/LRVSI/CRVSI); "reaseguro" es el
 * nombre del ítem de menú, no el alcance.
 */
@RestController
@RequestMapping("/v1/claim-accounting")
@CrossOrigin(origins = { "*" }, methods = { RequestMethod.POST, RequestMethod.GET })
public interface ClaimAccountingController extends BNPWebService {

	@GetMapping(path = "/accounting-date", produces = { "application/json" })
	BNPResponse getAccountingDate();

	@GetMapping(path = "/products", produces = { "application/json" })
	BNPResponse getProducts();

	@PostMapping(path = "/load", produces = { "application/json" })
	BNPResponse loadClaims(@Validated @RequestBody(required = true) LoadClaimRequestDto request);

	@PostMapping(path = "/generate", produces = { "application/json" })
	BNPResponse generateEntry(@Validated @RequestBody(required = true) GenerateAccountingRequestDto request);

	@PostMapping(path = "/register", produces = { "application/json" })
	BNPResponse registerEntry(@Validated @RequestBody(required = true) RegisterAccountingRequestDto request);

	@PostMapping(path = "/total-by-account", produces = { "application/json" })
	BNPResponse totalByAccount(@Validated @RequestBody(required = true) GenerateAccountingRequestDto request);

	@PostMapping(path = "/send", produces = { "application/json" })
	BNPResponse sendEntry(@Validated @RequestBody(required = true) SendAccountingRequestDto request);
}
