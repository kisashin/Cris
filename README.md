<div class="accounting-report-container">
  <div class="container-title">
    <h1 class="title">
      CIERRE MENSUAL DE DIRECTAS (CARDIF)
    </h1>
  </div>

  <section class="action-section">
    <span class="section-label">
      Reporte de movimientos:
    </span>
    <a [href]="reportMovement" target="_blank">Consultar</a>
  </section>

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
      {{ isGenerating ? 'GENERANDO...' : 'GENERA XML' }}
    </button>
  </section>

  @if (dataSource.length > 0) {
    <div class="container-table">
      <table mat-table [dataSource]="dataSource" class="mat-elevation-z8">
        <ng-container matColumnDef="processDate">
          <th mat-header-cell *matHeaderCellDef> FECHA PROCESO </th>
          <td mat-cell *matCellDef="let element"> {{ element.processDate }} </td>
        </ng-container>

        <ng-container matColumnDef="period">
          <th mat-header-cell *matHeaderCellDef> PERIODO </th>
          <td mat-cell *matCellDef="let element"> {{ element.period }} </td>
        </ng-container>

        <ng-container matColumnDef="family">
          <th mat-header-cell *matHeaderCellDef> ORIGEN </th>
          <td mat-cell *matCellDef="let element"> {{ element.family }} </td>
        </ng-container>

        <ng-container matColumnDef="movementType">
          <th mat-header-cell *matHeaderCellDef> TIPO MOVIMIENTO </th>
          <td mat-cell *matCellDef="let element"> {{ element.movementType }} </td>
        </ng-container>

        <ng-container matColumnDef="lineCount">
          <th mat-header-cell *matHeaderCellDef> LÍNEAS </th>
          <td mat-cell *matCellDef="let element"> {{ element.lineCount }} </td>
        </ng-container>

        <ng-container matColumnDef="status">
          <th mat-header-cell *matHeaderCellDef> ESTADO PROCESO </th>
          <td mat-cell *matCellDef="let element"> {{ element.status }} </td>
        </ng-container>

        <ng-container matColumnDef="action">
          <th mat-header-cell *matHeaderCellDef> REPORTES </th>
          <td mat-cell *matCellDef="let element">
            <a class="download-link" (click)="onDownloadXml(element)">
              Descargar XML
            </a>
          </td>
        </ng-container>

        <tr mat-header-row *matHeaderRowDef="displayedColumns"></tr>
        <tr mat-row *matRowDef="let row; columns: displayedColumns;"></tr>
      </table>
    </div>
  }
</div>
