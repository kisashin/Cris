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

        /* (bloque comentado existente ROLE_CO_CORE_*, sin cambios) */

        List<String> listPermisions = new ArrayList<>();

        listPermisions.add("PERM_CIE_PRD_VOBO_CARGUE");
        // listPermisions.add("PERM_CIE_PRD_HAB_VALIDACION");
        // listPermisions.add("PERM_CIE_PRD_VOBO_TRM");
        // listPermisions.add("PERM_CIE_PRD_VOBO_LEV_CIERRE");
        // listPermisions.add("PERM_CIE_PRD_VOBO_CIERRE");
        // listPermisions.add("PERM_CIE_PRD_MOD_CARGUE");
        listPermisions.add("PERM_CIE_VOBO_CIERRE");       // NUEVO: no existía en el mock
        listPermisions.add("PERM_CO_ANALYSIS_CIERRE");    // NUEVO: no existía en el mock

        /* (bloque comentado existente PERM_CORE_*, sin cambios) */

        response.setListRol(listRol);

        response.setListPermisions(listPermisions);       // DESCOMENTADO: sin esto los permisos no salen

        response.setInterfaceId(1);

        response.setNameFunctionary("Benjamin Rojas");

        response.setValid(Boolean.FALSE);

        return new BNPResponse(HttpStatus.OK, null, response);

    } catch (Exception e) {

        return new BNPResponse(HttpStatus.BAD_REQUEST, MSG503, null);

    }

}
