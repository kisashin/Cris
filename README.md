import { Component, Inject } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import {
  MAT_DIALOG_DATA,
  MatDialogModule,
  MatDialogRef
} from '@angular/material/dialog';
import { MatIconModule } from '@angular/material/icon';

import { IConfirmDialogData } from './confirm-dialog.model';

/**
 * Dialogo de confirmacion reutilizable para acciones destructivas.
 */
@Component({
  selector: 'app-confirm-dialog',
  imports: [MatDialogModule, MatButtonModule, MatIconModule],
  standalone: true,
  templateUrl: './confirm-dialog.component.html',
  styleUrl: './confirm-dialog.component.scss'
})
export class ConfirmDialogComponent {

  public readonly confirmText: string;
  public readonly cancelText: string;

  constructor(
    private readonly dialogRef: MatDialogRef<ConfirmDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public readonly data: IConfirmDialogData
  ) {
    this.confirmText = data?.confirmText ?? 'SÍ';
    this.cancelText = data?.cancelText ?? 'NO';
  }

  /**
   * Cierra el dialogo aceptando la accion.
   */
  public confirm(): void {
    this.dialogRef.close(true);
  }

  /**
   * Cierra el dialogo cancelando la accion.
   */
  public cancel(): void {
    this.dialogRef.close(false);
  }
}
