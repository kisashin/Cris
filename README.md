/* Tokens tomados de peru-accounting-report para mantener el mismo sistema:
   verde #006600 (marca), hover #004d00, disabled #7aa87a,
   Franklin Gothic Medium, uppercase en botones, error #a40000/#fdeaea. */

.accounting-entry-container {
  width: 100%;
  padding: 1rem 0;
}

/* ---------- Título ---------- */

.container-title {
  padding-bottom: 3rem;

  .title {
    margin: 0;
    color: #006600;
    font-family: 'Franklin Gothic Medium', Arial, sans-serif;
    font-size: 14pt;
    font-weight: 600;
  }
}

/* ---------- Fecha contable / producto ---------- */

.generation-section {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.row {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 1.5rem;
}

.field {
  display: flex;
  flex-direction: column;
  min-width: 180px;
}

.label,
.section-label {
  color: #006600;
  font-family: 'Franklin Gothic Medium', Arial, sans-serif;
  font-size: 14px;
  font-weight: 600;
}

.label {
  margin-bottom: .5rem;
}

/* Valor de la fecha contable */
.text-primary-color {
  color: #006600;
  font-family: 'Franklin Gothic Medium', Arial, sans-serif;
  font-size: 15px;
  font-weight: 600;
}

/* ---------- Comentario ---------- */

.comment-section {
  margin-bottom: 2rem;
}

.comment-field {
  width: 420px;
  max-width: 100%;
}

/* ---------- Botones ---------- */

.actions-section {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 2rem;
}

/* Botón estándar verde (Cargar, Generar, Registrar, Total x Cuenta) */
.action-button {
  min-height: 40px;
  min-width: 150px;
  padding: 0 1.25rem;
  color: #ffffff !important;
  background-color: #006600 !important;
  font-family: 'Franklin Gothic Medium', Arial, sans-serif;
  font-weight: 500;
  text-transform: uppercase;

  mat-icon {
    margin-right: 6px;
  }

  &:hover:not(:disabled) {
    background-color: #004d00 !important;
  }

  &:disabled {
    color: rgba(255, 255, 255, 0.7) !important;
    background-color: #7aa87a !important;
    cursor: not-allowed;
  }
}

/* Enviar: acción final/irreversible. En el legacy iba en rojo, se conserva
   esa señal pero con el mismo formato que los demás. */
.send-button {
  min-height: 40px;
  min-width: 150px;
  padding: 0 1.25rem;
  color: #ffffff !important;
  background-color: #a40000 !important;
  font-family: 'Franklin Gothic Medium', Arial, sans-serif;
  font-weight: 500;
  text-transform: uppercase;

  &:hover:not(:disabled) {
    background-color: #7d0000 !important;
  }

  &:disabled {
    color: rgba(255, 255, 255, 0.7) !important;
    background-color: #c98080 !important;
    cursor: not-allowed;
  }
}

/* ---------- Mensajes ---------- */

.message-section {
  width: 100%;
  margin-bottom: 1.5rem;
}

/* Mensaje de carga / error (mismo patrón que .error-message de Perú) */
.message {
  display: block;
  width: 100%;
  max-width: 700px;
  margin: 0 0 1.5rem;
  padding: 0.75rem 1rem;
  color: #a40000;
  background-color: #fdeaea;
  border: 1px solid #d60000;
  border-radius: 4px;
  font-size: 13px;
}

/* Confirmación (registrado / enviado) */
.success-message {
  display: block;
  width: 100%;
  max-width: 700px;
  margin: 0 0 1.5rem;
  padding: 0.75rem 1rem;
  color: #006600;
  background-color: #eaf5ea;
  border: 1px solid #006600;
  border-radius: 4px;
  font-size: 13px;
}

/* ---------- Tabla ---------- */
/* La tabla la pinta <app-report-table> (componente compartido de
   claims-closing). NO se estiliza aquí para no alterar los demás módulos
   que lo usan (Aval, Cardif, Homologación, Perú...). */

.container-table {
  width: 100%;
  margin-top: 2rem;
  overflow-x: auto;
}

/* ---------- Ancho uniforme de los form-field ---------- */

::ng-deep .mat-mdc-form-field {
  width: 250px;
}

/* ---------- Responsive (igual que Perú) ---------- */

@media (max-width: 768px) {

  .accounting-entry-container {
    padding: 1rem;
  }

  .container-title {
    padding-bottom: 2rem;
  }

  .generation-section,
  .row {
    align-items: flex-start;
    flex-direction: column;
    gap: 1rem;
  }

  .comment-field {
    width: 100%;
  }

  .actions-section {
    align-items: stretch;
    flex-direction: column;
  }

  .action-button,
  .send-button {
    width: 100%;
  }
}
