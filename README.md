<div>

  <div class="container-title">

    <h1 class="title">
      REPORTE DE DATOS (MOVIMIENTO ONBASE CENTROAMERICA)
    </h1>

  </div>

  <hr>

  <div class="container-generate">

    <span class="generate-text">
      Genere la información para el reporte de Datos y Movimientos
    </span>

    <button
      mat-raised-button
      color="primary"
      type="button"
      [disabled]="loading"
      (click)="generateInformation()">

      GENERAR

    </button>

  </div>

  <hr>

  <div class="container-title-table">

    <h2>
      Estado del Reporte
    </h2>

  </div>

  <div class="container-table">

    <table
      mat-table
      [dataSource]="reportStatus"
      class="report-status-table">

      <ng-container matColumnDef="fechaproceso">

        <th
          mat-header-cell
          *matHeaderCellDef>

          Fecha Proceso

        </th>

        <td
          mat-cell
          *matCellDef="let row">

          {{ row.fechaproceso | date:'dd/MM/yyyy HH:mm' }}

        </td>

      </ng-container>

      <ng-container matColumnDef="reportes">

        <th
          mat-header-cell
          *matHeaderCellDef>

          Reportes

        </th>

        <td
          mat-cell
          *matCellDef="let row">

          <button
            mat-raised-button
            color="primary"
            type="button"
            class="btn-report"
            [disabled]="loading"
            (click)="downloadData()">

            Rpt Datos

          </button>

          <button
            mat-raised-button
            color="primary"
            type="button"
            class="btn-report"
            [disabled]="loading"
            (click)="downloadMovements()">

            Rpt Movimientos

          </button>

        </td>

      </ng-container>

      <tr
        mat-header-row
        *matHeaderRowDef="statusColumns">
      </tr>

      <tr
        mat-row
        *matRowDef="let row; columns: statusColumns;">
      </tr>

    </table>

  </div>

  <hr>

  <div class="container-title-table">

    <h2>
      Coberturas Inconsistentes
    </h2>

  </div>

  <div
    *ngIf="inconsistentCoverages.length === 0"
    class="empty-information">

    No hay registros para mostrar.

  </div>

  <div
    *ngIf="inconsistentCoverages.length > 0"
    class="container-table">

    <app-report-table
      [dataSource]="pagedInconsistentCoverages"
      [displayedColumns]="displayedColumnsCoverage">
    </app-report-table>

    <mat-paginator
      [length]="coverageTotalElements"
      [pageIndex]="coveragePageIndex"
      [pageSize]="coveragePageSize"
      [pageSizeOptions]="[10]"
      (page)="changeCoveragePage($event)">
    </mat-paginator>

  </div>

  <div
    class="container-loading"
    *ngIf="loading">

    <mat-spinner diameter="45">
    </mat-spinner>

  </div>

</div>
