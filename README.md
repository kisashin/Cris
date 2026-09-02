export class CardifPeruClosingComponent {

  public readonly showGenerateXml = false;

  public errorMessage = '';
  public isGenerating = false;
  public isDownloading = false;




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
