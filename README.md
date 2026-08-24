import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { HttpResponse } from '@angular/common/http';
import { MatButtonModule } from '@angular/material/button';
import { MatTableModule } from '@angular/material/table';
import { ToastrService } from 'ngx-toastr';

import { AccountingClosingCaService } from '../../services/accounting-closing-ca.service';
import {
  IAccountingXmlFile,
  ICenterAccountingResult
} from '../../models/center-accounting-result.model';

/**
 * Pantalla Cierre Mensual (Centroamerica).
 */
@Component({
  selector: 'app-accounting-closing-ca',
  imports: [CommonModule, MatTableModule, MatButtonModule],
  standalone: true,
  templateUrl: './accounting-closing-ca.component.html',
  styleUrl: './accounting-closing-ca.component.scss'
})
export class AccountingClosingCAComponent {

  private static readonly XML_CONTENT_TYPE = 'application/xml';

  public isGenerating = false;
  public isDownloading = false;
  public dataSource: any[] = [];

  public readonly displayedColumns: string[] = [
    'processDate',
    'movementType',
    'status',
    'action'
  ];

  constructor(
    private readonly accountingClosingCaService: AccountingClosingCaService,
    private readonly toastr: ToastrService
  ) {}

  /**
   * Ejecuta la generacion de los asientos contables.
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
          const result = response?.bodyResponse ?? null;

          this.dataSource = this.buildRows(result);
          this.toastr.success(
            result?.message ?? 'Proceso ejecutado correctamente.'
          );
          this.isGenerating = false;
        },
        error: error => {
          console.error(
            'Error generating Centroamerica accounting entries:',
            error
          );

          this.dataSource = [];
          this.toastr.error(
            'No fue posible generar los asientos contables.'
          );
          this.isGenerating = false;
        }
      });
  }

  /**
   * Descarga el XML de la fila seleccionada.
   */
  public onDownloadXml(row: any): void {
    const file: IAccountingXmlFile = row?.file;

    if (!file?.content) {
      this.toastr.warning(
        'El archivo generado no contiene información.'
      );
      return;
    }

    this.saveFile(this.decodeBase64(file.content), file.fileName);
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

  private buildRows(result: ICenterAccountingResult | null): any[] {
    if (!result?.files?.length) {
      return [];
    }

    return result.files.map(file => ({
      processDate: result.processDate,
      movementType: file.movementType,
      status: result.status,
      file
    }));
  }

  private decodeBase64(content: string): Blob {
    const binary = window.atob(content);
    const bytes = new Uint8Array(binary.length);

    for (let index = 0; index < binary.length; index++) {
      bytes[index] = binary.charCodeAt(index);
    }

    return new Blob(
      [bytes],
      { type: AccountingClosingCAComponent.XML_CONTENT_TYPE }
    );
  }

  private saveExcelFile(response: HttpResponse<Blob>): void {
    const file = response.body;

    if (!file || file.size === 0) {
      this.toastr.warning(
        'El archivo generado no contiene información.'
      );
      return;
    }

    this.saveFile(file, this.getFileName(response));

    this.toastr.success(
      'Reporte descargado correctamente.'
    );
  }

  private saveFile(file: Blob, fileName: string): void {
    const objectUrl = window.URL.createObjectURL(file);
    const anchor = document.createElement('a');

    anchor.href = objectUrl;
    anchor.download = fileName;
    anchor.click();

    window.URL.revokeObjectURL(objectUrl);
  }

  private getFileName(response: HttpResponse<Blob>): string {
    const contentDisposition =
      response.headers.get('Content-Disposition');

    const fileNameMatch = contentDisposition?.match(
      /filename="?([^"]+)"?/
    );

    return fileNameMatch?.[1] ?? 'ReporteMovimientosCentro.xlsx';
  }
}
