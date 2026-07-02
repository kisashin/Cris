import { Component } from '@angular/core';
import { HttpResponse } from '@angular/common/http';
import { ToastrService } from 'ngx-toastr';

import { AccountingClosingCaService } from '../../services/accounting-closing-ca.service';

/**
 * Pantalla "Cierre Mensual (Centroamérica)" (legacy AsientoCardifCentro.aspx).
 *
 * <p>Dos acciones independientes: generar los asientos contables (ejecuta el
 * procedimiento en el backend) y consultar/descargar el reporte de movimientos
 * en Excel. El mensaje del Toast de generación proviene del backend.</p>
 */
@Component({
  selector: 'app-accounting-closing-ca',
  imports: [],
  standalone: true,
  templateUrl: './accounting-closing-ca.component.html',
  styleUrl: './accounting-closing-ca.component.scss',
})
export class AccountingClosingCAComponent {

  public isGenerating = false;
  public isDownloading = false;

  constructor(
    private readonly accountingClosingCaService: AccountingClosingCaService,
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

    this.accountingClosingCaService
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
            'Error generating Centroamerica accounting entries:',
            error
          );

          this.toastr.error(
            'No fue posible generar los asientos contables.'
          );
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

    this.accountingClosingCaService
      .downloadMovementsReport()
      .subscribe({
        next: response => {
          this.saveExcelFile(response);
          this.isDownloading = false;
        },
        error: error => {
          console.error(
            'Error downloading the Centroamerica movements report:',
            error
          );

          this.toastr.error(
            'No fue posible descargar el reporte de movimientos.'
          );
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
      'ReporteMovimientosCentro.xlsx';
  }
}
