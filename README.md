src/app/views/claims-closing/movements-peru/peru-accounting-report/peru-accounting-report.component.html

<div class="accounting-report-container">

  <div class="container-title">
    <h1 class="title">
      REPORTE CONTABLE (MOVIMIENTO ONBASE PERÚ)
    </h1>
  </div>

  <section class="generation-section">
    <span class="section-label">
      Cargar información reporte contable:
    </span>

    <button
      mat-raised-button
      color="primary"
      type="button"
      class="action-button"
      [disabled]="isGenerating"
      (click)="generateReport()">

      <mat-icon>refresh</mat-icon>

      {{ isGenerating ? 'GENERANDO...' : 'GENERAR' }}
    </button>
  </section>

  @if (errorMessage) {
    <div class="error-message" role="alert">
      {{ errorMessage }}
    </div>
  }

  <section class="previous-report-section">

    <h2 class="section-title">
      Reporte anterior:
    </h2>

    <div class="report-table-container">

      <table class="report-table">
        <thead>
          <tr>
            <th>FECHA REPORTE</th>
            <th>REPORTES</th>
          </tr>
        </thead>

        <tbody>
          <tr>
            <td>
              @if (isLoadingDate) {
                <span>Consultando...</span>
              } @else if (reportDate) {
                <span>
                  {{ reportDate | date:'dd/MM/yyyy h:mm:ss a' }}
                </span>
              } @else {
                <span>Sin información disponible</span>
              }
            </td>

            <td>
              <button
                mat-raised-button
                color="primary"
                type="button"
                class="download-button"
                [disabled]="isDownloading || !reportDate"
                (click)="downloadReport()">

                <mat-icon>download</mat-icon>

                {{
                  isDownloading
                    ? 'DESCARGANDO...'
                    : 'GENERAR REPORTE'
                }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>

    </div>
  </section>

</div>
