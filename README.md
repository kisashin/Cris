<div>
    <div class="container-title">
        <h1 class="title">Cierre Mensual de Aval</h1>
    </div>
    <div>
      <span class="text-primary-color">Reporte de movimientos: </span>
      <a [href]="reportMovement"
        target="_blank">Consultar</a>
    </div>
    <br>

    @if (!hasAvalData && !isLoadingReport) {
      <p class="mt-2 text-muted">No registros para consultar</p>
    }

    @if (hasAvalData) {
      <div class="container-table">
        <table mat-table [dataSource]="dataSourceAval" class="mat-elevation-z8">
          <ng-container matColumnDef="dateGenerate">
            <th mat-header-cell *matHeaderCellDef>
              FECHA DEL REPORTE MENSUAL DE AVAL
            </th>
            <td mat-cell *matCellDef="let element"> {{ element.dateGenerate }} </td>
          </ng-container>

          <ng-container matColumnDef="status">
            <th mat-header-cell *matHeaderCellDef> ESTADO PROCESO </th>
            <td mat-cell *matCellDef="let element"> {{ element.status }} </td>
          </ng-container>

          <ng-container matColumnDef="nombreRpt">
            <th mat-header-cell *matHeaderCellDef> REPORTE </th>
            <td mat-cell *matCellDef="let element"> {{ element.nombreRpt }} </td>
          </ng-container>

          <ng-container matColumnDef="actions">
            <th mat-header-cell *matHeaderCellDef> ACCIONES </th>
            <td mat-cell *matCellDef="let element">
              <button
                mat-button
                type="button"
                [disabled]="isLoadingReport"
                (click)="generateAval()">
                GENERAR
              </button>
            </td>
          </ng-container>

          <tr mat-header-row *matHeaderRowDef="displayedColumnsAval"></tr>
          <tr mat-row *matRowDef="let row; columns: displayedColumnsAval;"></tr>
        </table>
      </div>
    }

    <section class="action-section mt-4">
      <span class="text-primary-color span-text-status-report">
        Generación de Asientos Contables:
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
