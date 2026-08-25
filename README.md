<h2 mat-dialog-title class="dialog-title">
  <mat-icon class="dialog-icon">warning</mat-icon>
  {{ data.title }}
</h2>

<mat-dialog-content class="dialog-content">
  {{ data.message }}
</mat-dialog-content>

<mat-dialog-actions class="dialog-actions">
  <button
    mat-stroked-button
    type="button"
    class="cancel-button"
    (click)="cancel()">
    {{ cancelText }}
  </button>

  <button
    mat-raised-button
    color="primary"
    type="button"
    class="confirm-button"
    (click)="confirm()">
    {{ confirmText }}
  </button>
</mat-dialog-actions>
