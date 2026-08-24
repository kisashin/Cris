<div>
    <div class="container-title">
        <h1 class="title">Cierre Mensual (Centroamérica) </h1>
    </div>
    <div>
        <span class="text-primary-color">Reporte de movimientos: </span>
        <a class="link-action" (click)="downloadReport()">
            {{ isDownloading ? 'Descargando...' : 'Consultar' }}
        </a>
    </div>
    <br>

    <div>
        <span class="text-primary-color span-text-status-report">Generación de Asientos Contables: </span>
        <button
            mat-raised-button
            type="button"
            class="action-button"
            [disabled]="isGenerating"
            (click)="generateAccountingEntries()">
            {{ isGenerating ? 'GENERANDO...' : 'GENERAR XML' }}
        </button>

        <div class="table-responsive container-table" *ngIf="dataSource.length > 0">
            <table mat-table [dataSource]="dataSource" class="mat-elevation-z8">
                <ng-container matColumnDef="processDate">
                    <th mat-header-cell *matHeaderCellDef class="mat-header-cell"> FECHA PROCESO </th>
                    <td mat-cell *matCellDef="let element"> {{ element.processDate }} </td>
                </ng-container>

                <ng-container matColumnDef="period">
                    <th mat-header-cell *matHeaderCellDef class="mat-header-cell"> PERIODO </th>
                    <td mat-cell *matCellDef="let element"> {{ element.period }} </td>
                </ng-container>

                <ng-container matColumnDef="movementType">
                    <th mat-header-cell *matHeaderCellDef class="mat-header-cell"> TIPO MOVIMIENTO </th>
                    <td mat-cell *matCellDef="let element"> {{ element.movementType }} </td>
                </ng-container>

                <ng-container matColumnDef="lineCount">
                    <th mat-header-cell *matHeaderCellDef class="mat-header-cell"> LÍNEAS </th>
                    <td mat-cell *matCellDef="let element"> {{ element.lineCount }} </td>
                </ng-container>

                <ng-container matColumnDef="status">
                    <th mat-header-cell *matHeaderCellDef class="mat-header-cell"> ESTADO PROCESO </th>
                    <td mat-cell *matCellDef="let element"> {{ element.status }} </td>
                </ng-container>

                <ng-container matColumnDef="action">
                    <th mat-header-cell *matHeaderCellDef class="mat-header-cell"> REPORTES </th>
                    <td mat-cell *matCellDef="let element">
                        <button mat-button (click)="onDownloadXml(element)">
                            Descargar XML
                        </button>
                    </td>
                </ng-container>

                <tr mat-header-row *matHeaderRowDef="displayedColumns"></tr>
                <tr mat-row *matRowDef="let row; columns: displayedColumns;"></tr>
            </table>
        </div>
    </div>
</div>
