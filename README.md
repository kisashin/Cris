import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { HttpResponse } from '@angular/common/http';
import { MatButtonModule } from '@angular/material/button';
import { MatTableModule } from '@angular/material/table';
import { ToastrService } from 'ngx-toastr';

import { AccountingClosingCaService } from '../../services/accounting-closing-ca.service';
import { IAccountingXmlFile } from '../../models/center-accounting-result.model';

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
export class AccountingClosingCAComponent implements OnInit {

  public isGenerating = false;
  public isDownloading = false;
  public isLoading = false;
  public dataSource: IAccountingXmlFile[] = [];

  public readonly displayedColumns: string[] = [
    'processDate',
    'period',
    'movementType',
    'lineCount',
    'status',
    'action'
  ];

  constructor(
    private readonly accountingClosingCaService: AccountingClosingCaService,
    private readonly toastr: ToastrService
  ) {}

  ngOnInit(): void {
    this.loadGeneratedFiles();
  }

  /**
   * Consulta los archivos generados en procesos anteriores.
   */
  public loadGeneratedFiles(): void {
    this.isLoading = true;

    this.accountingClosingCaService
      .findGeneratedFiles()
      .subscribe({
        next: response => {
          this.dataSource = response?.bodyResponse ?? [];
          this.isLoading = false;
        },
        error: error => {
          console.error(
            'Error loading Centroamerica accounting files:',
            error
          );

          this.dataSource = [];
          this.isLoading = false;
        }
      });
  }

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
          this.toastr.success(
            response?.bodyResponse?.message ??
            'Proceso ejecutado correctamente.'
          );
          this.isGenerating = false;
          this.loadGeneratedFiles();
        },
        error: error => {
          console.error(
            'Error generating Centroamerica accounting entries:',
            error
          );

          this.toastr.error(
            error?.error?.errorHeader?.errorMessage ??
            'No fue posible generar los asientos contables.'
          );
          this.isGenerating = false;
        }
      });
  }

  /**
   * Descarga el XML de la fila seleccionada.
   */
  public onDownloadXml(row: IAccountingXmlFile): void {
    this.accountingClosingCaService
      .downloadXmlFile(row.id)
      .subscribe({
        next: response => this.saveBlobFile(response, row.fileName),
        error: error => {
          console.error('Error downloading the XML file:', error);

          this.toastr.error(
            'No fue posible descargar el archivo XML.'
          );
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
          this.saveBlobFile(response, this.getFileName(response));
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

  private saveBlobFile(
    response: HttpResponse<Blob>,
    fileName: string
  ): void {
    const file = response.body;

    if (!file || file.size === 0) {
      this.toastr.warning(
        'El archivo generado no contiene información.'
      );
      return;
    }

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
