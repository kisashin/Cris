<div class="accounting-entry-container">

  <div class="container-title">
    <h1 class="title">
      ASIENTOS SINIESTROS
    </h1>
  </div>

  <section class="generation-section">

    <div class="field">
      <span class="section-label">Fecha contable:</span>
      <span class="text-primary-color">{{ accountingDate }}</span>
    </div>

    <div class="field">
      <mat-form-field appearance="outline">
        <mat-label>Producto</mat-label>
        <mat-select
          [(ngModel)]="selectedProduct"
          (selectionChange)="onProductChange()">
          <mat-option
            *ngFor="let product of products"
            [value]="product.product">
            {{ product.product }}
          </mat-option>
        </mat-select>
      </mat-form-field>
    </div>

  </section>

  <section class="upload-section">

    <span class="section-label">Archivo de siniestros:</span>

    <input
      type="file"
      accept=".csv"
      class="file-input"
      #fileInput
      (change)="onFileSelected($event)">

    <button
      mat-raised-button
      type="button"
      class="action-button"
      [disabled]="loading"
      (click)="fileInput.click()">

      <mat-icon>attach_file</mat-icon>

      SELECCIONAR
    </button>

    <span class="file-name" *ngIf="selectedFile">
      {{ selectedFile.name }}
    </span>

    <button
      mat-raised-button
      type="button"
      class="action-button"
      [disabled]="loading"
      (click)="loadClaims()">

      <mat-icon>upload</mat-icon>

      {{ loading ? 'CARGANDO...' : 'CARGAR' }}
    </button>

  </section>

  <section class="message-section" *ngIf="message">
    <span class="message">{{ message }}</span>
  </section>

  <section class="comment-section">
    <mat-form-field appearance="outline" class="comment-field">
      <mat-label>Comentario del asiento</mat-label>
      <input matInput [(ngModel)]="comment">
    </mat-form-field>
  </section>

  <section class="actions-section">

    <button
      mat-raised-button
      type="button"
      class="action-button"
      [disabled]="loading"
      (click)="generateAccountingEntry()">
      Generar Asiento
    </button>

    <button
      mat-raised-button
      type="button"
      class="action-button"
      [disabled]="loading"
      (click)="registerAccountingEntry()">
      Registrar Asiento
    </button>

    <button
      mat-raised-button
      type="button"
      class="action-button"
      [disabled]="loading"
      (click)="getAccountSummary()">
      Total x Cuenta
    </button>

    <button
      mat-raised-button
      type="button"
      class="send-button"
      [disabled]="loading"
      (click)="sendAccountingEntry()">
      Generar XML
    </button>

  </section>

  <section class="message-section" *ngIf="sendMessage">
    <span class="success-message">{{ sendMessage }}</span>
  </section>

  <div class="container-table" *ngIf="dataSource.length > 0">
    <app-report-table
      [dataSource]="dataSource"
      [displayedColumns]="displayedColumns">
    </app-report-table>
  </div>

  <div class="files-section" *ngIf="files.length > 0">

    <span class="section-label">Archivos generados del periodo:</span>

    <div class="container-table">
      <table mat-table [dataSource]="files" class="mat-elevation-z8">

        <ng-container matColumnDef="product">
          <th mat-header-cell *matHeaderCellDef> PRODUCTO </th>
          <td mat-cell *matCellDef="let element"> {{ element.product }} </td>
        </ng-container>

        <ng-container matColumnDef="journalType">
          <th mat-header-cell *matHeaderCellDef> TIPO DIARIO </th>
          <td mat-cell *matCellDef="let element"> {{ element.journalType }} </td>
        </ng-container>

        <ng-container matColumnDef="fileName">
          <th mat-header-cell *matHeaderCellDef> ARCHIVO </th>
          <td mat-cell *matCellDef="let element"> {{ element.fileName }} </td>
        </ng-container>

        <ng-container matColumnDef="generationDate">
          <th mat-header-cell *matHeaderCellDef> FECHA GENERACIÓN </th>
          <td mat-cell *matCellDef="let element"> {{ element.generationDate }} </td>
        </ng-container>

        <ng-container matColumnDef="action">
          <th mat-header-cell *matHeaderCellDef> DESCARGA </th>
          <td mat-cell *matCellDef="let element">
            <a class="download-link" (click)="onDownloadXml(element)">
              Descargar XML
            </a>
          </td>
        </ng-container>

        <tr mat-header-row *matHeaderRowDef="fileColumns"></tr>
        <tr mat-row *matRowDef="let row; columns: fileColumns;"></tr>
      </table>
    </div>

  </div>

</div>
