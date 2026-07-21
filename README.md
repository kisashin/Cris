} catch (Exception e) {
    log.error("Error en loadClaims", e);
    throw new DatabaseException(ExceptionConstants.DATABASE_CONNECTION, e);
}
