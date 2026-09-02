    { ruta: '/asientosSiniestros', icon: ' fact_check', tooltip: 'Asientos Siniestros',
      submenu: [
        {titulo: 'Reaseguro', url:['/accounting-entry'], external: false}
      ]
     },




        {titulo: 'Otros Tipos Referencia', url: ['/other-type-reference'], external: false},
        {titulo: 'Novedades Individuales', url: '', external: false}





    {
      route: '/accounting-entry',
      icon: 'assets/icons/icon-habilitacionErrores.svg',
      alt: 'Asientos Siniestros',
      label: 'Asientos Siniestros',
      size: 80
    },




      @if (showGenerateXml) {
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
  }
