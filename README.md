
src/app/views/claims-closing/movements-peru/cardif-peru-closing/cardif-peru-closing.component.html
src/app/views/claims-closing/movements-peru/cardif-peru-closing/cardif-peru-closing.component.scss
src/app/views/claims-closing/movements-peru/cardif-peru-closing/cardif-peru-closing.component.spec.ts



src/app/views/claims-closing/services/cardif-peru-closing.service.ts
src/app/views/claims-closing/services/cardif-peru-closing.service.spec.ts

<div class="accounting-report-container">

  <div class="container-title">
    <h1 class="title">
      CIERRE CARDIF (MOVIMIENTO ONBASE PERÚ)
    </h1>
  </div>

  <section class="action-section">
    <span class="section-label">
      Generación de asientos contables:
    </span>

    <button
      mat-raised-button
      color="primary"
      type="button"
      class="action-button"
      [disabled]="isGenerating"
      (click)="generateAccountingEntries()">

      <mat-icon>refresh</mat-icon>

      {{ isGenerating ? 'GENERANDO...' : 'GENERAR ASIENTOS' }}
    </button>
  </section>

  @if (errorMessage) {
    <div class="error-message" role="alert">
      {{ errorMessage }}
    </div>
  }

  <section class="action-section">
    <span class="section-label">
      Reporte de movimientos:
    </span>

    <button
      mat-raised-button
      color="primary"
      type="button"
      class="download-button"
      [disabled]="isDownloading"
      (click)="downloadReport()">

      <mat-icon>download</mat-icon>

      {{ isDownloading ? 'DESCARGANDO...' : 'CONSULTAR' }}
    </button>
  </section>

</div>
