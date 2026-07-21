<div class="accounting-entry-container">

  <div class="container-title">
    <h1 class="title">
      ASIENTOS SINIESTROS (REASEGURO)
    </h1>
  </div>

  <section class="generation-section">

    <div class="field">
      <span class="section-label">Fecha contable:</span>
      <span class="text-primary-color">{{ accountingDate }}</span>
    </div>

    <div class="field">
      <mat-form-field appearance="outline">
        <mat-label>Producto</mat-label>
        <mat-select
          [(ngModel)]="selectedProduct"
          (selectionChange)="onProductChange()">
          <mat-option
            *ngFor="let product of products"
            [value]="product.product">
            {{ product.product }}
          </mat-option>
        </mat-select>
      </mat-form-field>
    </div>

    <button
      mat-raised-button
      type="button"
      class="action-button"
      [disabled]="loading"
      (click)="loadClaims()">
      {{ loading ? 'CARGANDO...' : 'CARGAR' }}
    </button>

  </section>

  <section class="message-section" *ngIf="message">
    <span class="message">{{ message }}</span>
  </section>

  <section class="comment-section">
    <mat-form-field appearance="outline" class="comment-field">
      <mat-label>Comentario del asiento</mat-label>
      <input matInput [(ngModel)]="comment">
    </mat-form-field>
  </section>

  <section class="actions-section">

    <button
      mat-raised-button
      type="button"
      class="action-button"
      [disabled]="loading"
      (click)="generateAccountingEntry()">
      Generar Asiento
    </button>

    <button
      mat-raised-button
      type="button"
      class="action-button"
      [disabled]="loading"
      (click)="registerAccountingEntry()">
      Registrar Asiento
    </button>

    <button
      mat-raised-button
      type="button"
      class="action-button"
      [disabled]="loading"
      (click)="getAccountSummary()">
      Total x Cuenta
    </button>

    <button
      mat-raised-button
      type="button"
      class="send-button"
      [disabled]="loading"
      (click)="sendAccountingEntry()">
      Enviar
    </button>

  </section>

  <section class="message-section" *ngIf="sendMessage">
    <span class="success-message">{{ sendMessage }}</span>
  </section>

  <div class="container-table" *ngIf="dataSource.length > 0">
    <app-report-table
      [dataSource]="dataSource"
      [displayedColumns]="displayedColumns">
    </app-report-table>
  </div>

</div>





.accounting-entry-container {
  width: 100%;
  padding: 1rem 0;
}

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

.generation-section {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.field {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.section-label {
  margin-bottom: .5rem;
  color: #006600;
  font-family: 'Franklin Gothic Medium', Arial, sans-serif;
  font-size: 14px;
  font-weight: 600;
}

.text-primary-color {
  color: #006600;
  font-family: 'Franklin Gothic Medium', Arial, sans-serif;
  font-size: 15px;
  font-weight: 600;
}

.comment-section {
  margin-bottom: 2rem;
}

.comment-field {
  width: 420px;
  max-width: 100%;
}

.actions-section {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 2rem;
}

.action-button {
  min-height: 40px;
  min-width: 170px;
  padding: 0 1.25rem;
  color: #ffffff !important;
  background-color: #006600 !important;
  font-family: 'Franklin Gothic Medium', Arial, sans-serif;
  font-weight: 500;
  text-transform: uppercase;

  &:hover:not(:disabled) {
    background-color: #004d00 !important;
  }

  &:disabled {
    color: rgba(255, 255, 255, 0.7) !important;
    background-color: #7aa87a !important;
    cursor: not-allowed;
  }
}

.send-button {
  min-height: 40px;
  min-width: 170px;
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

.message-section {
  width: 100%;
  margin-bottom: 1.5rem;
}

.message {
  display: block;
  width: 100%;
  max-width: 700px;
  margin: 0;
  padding: 0.75rem 1rem;
  color: #a40000;
  background-color: #fdeaea;
  border: 1px solid #d60000;
  border-radius: 4px;
  font-size: 13px;
}

.success-message {
  display: block;
  width: 100%;
  max-width: 700px;
  margin: 0;
  padding: 0.75rem 1rem;
  color: #006600;
  background-color: #eaf5ea;
  border: 1px solid #006600;
  border-radius: 4px;
  font-size: 13px;
}

.container-table {
  width: 100%;
  margin-top: 2rem;
  overflow-x: auto;
}

::ng-deep .accounting-entry-container {

  .mat-mdc-form-field {
    width: 250px;
  }

  .mdc-notched-outline__leading,
  .mdc-notched-outline__notch,
  .mdc-notched-outline__trailing {
    border-color: #006600;
  }

  .mdc-floating-label,
  .mat-mdc-select-arrow,
  .mat-mdc-select-value {
    color: #006600;
  }
}

@media (max-width: 768px) {

  .accounting-entry-container {
    padding: 1rem;
  }

  .container-title {
    padding-bottom: 2rem;
  }

  .generation-section {
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
