    <div class="container-table">
      <table mat-table [dataSource]="reportDataSource" class="mat-elevation-z8">
        <ng-container matColumnDef="processDate">
          <th mat-header-cell *matHeaderCellDef> FECHA PROCESO </th>
          <td mat-cell *matCellDef="let element">
            {{ element.processDate || '—' }}
          </td>
        </ng-container>

        <ng-container matColumnDef="reportStatus">
          <th mat-header-cell *matHeaderCellDef> ESTADO </th>
          <td mat-cell *matCellDef="let element">
            {{ getReportStatusLabel(element) }}
          </td>
        </ng-container>

        <ng-container matColumnDef="actions">
          <th mat-header-cell *matHeaderCellDef> ACCIONES </th>
          <td mat-cell *matCellDef="let element">
            <button
              mat-button
              type="button"
              [disabled]="isGeneratingReport"
              (click)="generateReport(element)">
              {{ isGeneratingReport ? 'GENERANDO...' : 'GENERAR' }}
            </button>
          </td>
        </ng-container>

        <ng-container matColumnDef="action">
          <th mat-header-cell *matHeaderCellDef> REPORTE </th>
          <td mat-cell *matCellDef="let element">
            @if (element.id) {
              <a class="download-link" (click)="downloadReport(element)">
                {{ isDownloadingReport ? 'DESCARGANDO...' : 'Descargar Excel' }}
              </a>
            } @else {
              —
            }
          </td>
        </ng-container>

        <tr mat-header-row *matHeaderRowDef="displayedColumnsReport"></tr>
        <tr mat-row *matRowDef="let row; columns: displayedColumnsReport;"></tr>
      </table>
    </div>
