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
<div>
    <span class="text-primary-color">Generación de Asientos Contables: </span>
    <button
        type="button"
        class="btn btn-success ml-3"
        [disabled]="isGenerating"
        (click)="generateAccountingEntries()">
        {{ isGenerating ? 'Generando...' : 'Generar XML' }}
    </button>
</div>
