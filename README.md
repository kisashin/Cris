src/app/views/claims-closing/movements-peru/cardif-peru-closing/cardif-peru-closing.component.ts
src/app/views/claims-closing/movements-peru/cardif-peru-closing/cardif-peru-closing.component.html
src/app/views/claims-closing/movements-peru/cardif-peru-closing/cardif-peru-closing.component.scss
src/app/views/claims-closing/movements-peru/cardif-peru-closing/cardif-peru-closing.component.spec.ts



src/app/views/claims-closing/services/cardif-peru-closing.service.ts
src/app/views/claims-closing/services/cardif-peru-closing.service.spec.ts

import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { HttpResponse } from '@angular/common/http';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { ToastrService } from 'ngx-toastr';

import { CardifPeruClosingService } from '../../services/cardif-peru-closing.service';

/**
 * Pantalla "Cierre Cardif Perú" (legacy AsientoCardif_ext.aspx).
 *
 * <p>Dos acciones independientes: generar los asientos contables (ejecuta el
 * procedimiento en el backend) y consultar/descargar el reporte de movimientos
 * en Excel. El mensaje del Toast de generación proviene del backend, no se
 * fija en el front.</p>
 */
@Component({
  selector: 'app-cardif-peru-closing',
  standalone: true,
  imports: [
    CommonModule,
    MatButtonModule,
    MatIconModule
  ],
  templateUrl: './cardif-peru-closing.component.html',
  styleUrl: './cardif-peru-closing.component.scss'
})
export class CardifPeruClosingComponent {

  public errorMessage = '';

  public isGenerating = false;
  public isDownloading = false;

  constructor(
    private readonly cardifPeruClosingService: CardifPeruClosingService,
    private readonly toastr: ToastrService
  ) {}

  /**
   * Ejecuta la generación de los asientos contables.
   */
  public generateAccountingEntries(): void {
    if (this.isGenerating) {
      return;
    }

    this.isGenerating = true;
    this.errorMessage = '';

    this.cardifPeruClosingService
      .generateAccountingEntries()
      .subscribe({
        next: response => {
          const message =
            response?.bodyResponse ||
            'Proceso ejecutado correctamente.';

          this.toastr.success(message);
          this.isGenerating = false;
        },
        error: error => {
          console.error(
            'Error generating Cardif Peru accounting entries:',
            error
          );

          this.errorMessage =
            'No fue posible generar los asientos contables.';
          this.toastr.error(this.errorMessage);
          this.isGenerating = false;
        }
      });
  }

  /**
   * Descarga el reporte de movimientos en formato Excel.
   */
  public downloadReport(): void {
    if (this.isDownloading) {
      return;
    }

    this.isDownloading = true;
    this.errorMessage = '';

    this.cardifPeruClosingService
      .downloadMovementsReport()
      .subscribe({
        next: response => {
          this.saveExcelFile(response);
          this.isDownloading = false;
        },
        error: error => {
          console.error(
            'Error downloading the Cardif Peru movements report:',
            error
          );

          this.errorMessage =
            'No fue posible descargar el reporte de movimientos.';
          this.toastr.error(this.errorMessage);
          this.isDownloading = false;
        }
      });
  }

  private saveExcelFile(
    response: HttpResponse<Blob>
  ): void {
    const file = response.body;

    if (!file || file.size === 0) {
      this.toastr.warning(
        'El archivo generado no contiene información.'
      );
      return;
    }

    const fileName = this.getFileName(response);
    const objectUrl = window.URL.createObjectURL(file);
    const anchor = document.createElement('a');

    anchor.href = objectUrl;
    anchor.download = fileName;
    anchor.click();

    window.URL.revokeObjectURL(objectUrl);

    this.toastr.success(
      'Reporte descargado correctamente.'
    );
  }

  private getFileName(
    response: HttpResponse<Blob>
  ): string {
    const contentDisposition =
      response.headers.get('Content-Disposition');

    const fileNameMatch = contentDisposition?.match(
      /filename="?([^"]+)"?/
    );

    return fileNameMatch?.[1] ??
      'ReporteMovimientosCardifPeru.xlsx';
  }
}
