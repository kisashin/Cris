<div class="container-title">
    <h1 class="title text-primary-color">CIERRE MENSUAL (CENTROAMERICA)</h1>
</div>
<div class="container-report-movements">
    <span class="text-primary-color">Reporte de movimientos: </span>
    <button
        type="button"
        class="btn btn-success ml-3"
        [disabled]="isDownloading"
        (click)="downloadReport()">
        {{ isDownloading ? 'Descargando...' : 'Consultar' }}
    </button>
</div>
<div class="container-accounting-entries">
    <span class="text-primary-color">Generación de Asientos Contables: </span>
    <button
        type="button"
        class="btn btn-success ml-3"
        [disabled]="isGenerating"
        (click)="generateAccountingEntries()">
        {{ isGenerating ? 'Generando...' : 'Generar XML' }}
    </button>
</div>
<table class="accounting-table" *ngIf="result?.files?.length">
    <thead>
        <tr>
            <th>FECHA PROCESO</th>
            <th>TIPO MOVIMIENTO</th>
            <th>ESTADO PROCESO</th>
            <th>REPORTES</th>
        </tr>
    </thead>
    <tbody>
        <tr *ngFor="let file of result?.files">
            <td>{{ result?.processDate }}</td>
            <td>{{ file.movementType }}</td>
            <td>{{ result?.status }}</td>
            <td>
                <a
                    href="javascript:void(0)"
                    class="download-link"
                    (click)="downloadXmlFile(file)">
                    Descargar XML
                </a>
            </td>
        </tr>
    </tbody>
</table>
