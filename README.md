package co.com.bnpparibas.cardif.authenticateServices.controller.impl;



import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.stereotype.Component;
import org.springframework.web.servlet.ModelAndView;

import co.com.bnpparibas.cardif.authenticateServices.controller.ISsoAuthenticate;
import co.com.bnpparibas.cardif.authenticateServices.service.ISsoAuthenticateService;
import co.com.bnpparibas.cardif.authenticateServices.util.exception.WsSsoCoException;
import co.com.bnpparibas.cardif.transversal.model.BNPAuthenticateInitializer;
import co.com.bnpparibas.cardif.transversal.model.BNPAuthenticated;
import co.com.bnpparibas.cardif.transversal.model.BNPLogin;
import co.com.bnpparibas.webservicemask.model.ws.response.BNPResponse;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Iterator;
import java.util.List;

@Component("ssoAuthenticate")
public class SsoAuthenticate implements ISsoAuthenticate {

	public static final String MSG500 = "Error contacte con soporte";
	public static final String MSG501 = "No se logro recuperar llave publica.";
	public static final String MSG502 = "Error solicitando llave publica";
	public static final String MSG503 = "Error autenticando usuario";

	
	@Autowired
	private ISsoAuthenticateService iSsoAuthenticateService;

	@Override
	public BNPResponse publicKey() {
		try {
			BNPAuthenticateInitializer response = this.iSsoAuthenticateService.publicKey();
			if (response == null) {
				return new BNPResponse(HttpStatus.NO_CONTENT, MSG501);
			}
			 
			return new BNPResponse(HttpStatus.OK, null, response);
		} catch (WsSsoCoException e) {
			return new BNPResponse(HttpStatus.BAD_REQUEST, MSG502, null);
		}
	}

	@Override
	public BNPResponse login(BNPLogin login, String sessionId) {

		try {

          //BNPAuthenticated response = this.iSsoAuthenticateService.login(login, sessionId);

			BNPAuthenticated response = new BNPAuthenticated("2b20d3b3f9c747ba340b0c82f2c8f59a2b37308e", "f93141");

			List<String> listRol = new ArrayList<>();

            // listRol.add("R_CO_CIE_DIRECTOR");
            // listRol.add("R_CO_CIE_COORDINADOR");
            listRol.add("R_CO_CIE_ANALISTACIERRE");
            // listRol.add("R_CO_CIE_CIERRE");
            // listRol.add("R_CO_CIE_QA");
            // listRol.add("R_CO_CIE_PRODUCCION");
            // listRol.add("R_CO_CIE_ANALISTAPRD");
            // listRol.add("R_CO_CIE_ACTUARIA");
            // listRol.add("R_CO_CIE_CONFIGURATION");

			/*listRol.add("ROLE_CO_CORE_CONF_COVERAGE");

			listRol.add("ROLE_CO_CORE_VIEW_CLINICAL_DOC");

			listRol.add("ROLE_CO_CORE_ADMIN");
			listRol.add("ROLE_CO_CORE_MASTER_ADMIN");

			listRol.add("ROLE_CO_CORE_COUNTRY");
			listRol.add("ROLE_CO_CORE_COUNTRY_PERU");

			listRol.add("ROLE_CO_CORE_PUBLI_DOC");

			//listRol.add("authauth");*/

			List<String> listPermisions = new ArrayList<>();

            listPermisions.add("PERM_CIE_PRD_VOBO_CARGUE");
            // listPermisions.add("PERM_CIE_PRD_HAB_VALIDACION");
            // listPermisions.add("PERM_CIE_PRD_VOBO_TRM");
            // listPermisions.add("PERM_CIE_PRD_VOBO_LEV_CIERRE");
            // listPermisions.add("PERM_CIE_PRD_VOBO_CIERRE");
            // listPermisions.add("PERM_CIE_PRD_MOD_CARGUE");
            listPermisions.add("PERM_CIE_VOBO_CIERRE");
            listPermisions.add("PERM_CO_ANALYSIS_CIERRE");
			/*listPermisions.add("PERM_CORE_PAYMENT_SCHEDULING");

			listPermisions.add("PERM_CORE_ANALYSIS_DECISION");

			listPermisions.add("PERM_CORE_BOOKING_MANAGEMENT");

			listPermisions.add("PERM_CORE_STATE_HISTORY");

			listPermisions.add("PERM_CORE_UPLOAD_NEW_DOCUMENTS");

			listPermisions.add("PERM_CORE_ASSURED_INFORMATION");

			listPermisions.add("PERM_CORE_UPLOADED_DOCUMENTS");

			listPermisions.add("PERM_CORE_COVERAGE_ANALYSIS");

			listPermisions.add("PERM_CORE_OBSERVATION_HISTORY");

			listPermisions.add("PERM_CORE_VIEW_DOC");

			listPermisions.add("PERM_CORE_UPDATING_FIELDS");

			listPermisions.add("PERM_CORE_GENERAL_INFORMATION");

			listPermisions.add("PERM_CORE_VIEW_CONFIRM_COVERAGE");

			listPermisions.add("PERM_CORE_POLICY_INFORMATION");*/

			response.setListRol(listRol);

			response.setListPermisions(listPermisions);

			response.setInterfaceId(1);

			response.setNameFunctionary("Benjamin Rojas");

			response.setValid(Boolean.FALSE);

			return new BNPResponse(HttpStatus.OK, null, response);

		} catch (Exception e) {

			return new BNPResponse(HttpStatus.BAD_REQUEST, MSG503, null);

		}

	}



	@Override
	public ModelAndView dinamicKey(Authentication authentication, HttpServletRequest req, HttpServletResponse response) {
		return iSsoAuthenticateService.dinamicKey(authentication, req, response);
	}
}
