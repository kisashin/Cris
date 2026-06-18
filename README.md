src/app/views/claims-closing/movements-peru/peru-accounting-report/peru-accounting-report.component.ts

import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { HttpResponse } from '@angular/common/http';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { ToastrService } from 'ngx-toastr';

import { PeruAccountingReportService } from '../../services/peru-accounting-report.service';

@Component({
  selector: 'app-peru-accounting-report',
  standalone: true,
  imports: [
    CommonModule,
    MatButtonModule,
    MatIconModule
  ],
  templateUrl: './peru-accounting-report.component.html',
  styleUrl: './peru-accounting-report.component.scss'
})
export class PeruAccountingReportComponent implements OnInit {

  public reportDate: string | null = null;
  public errorMessage = '';

  public isLoadingDate = false;
  public isGenerating = false;
  public isDownloading = false;

  constructor(
    private readonly peruAccountingReportService:
      PeruAccountingReportService,
    private readonly toastr: ToastrService
  ) {}

  ngOnInit(): void {
    this.loadLatestReportDate();
  }

  /**
   * Consulta la fecha de la última generación del reporte.
   */
  public loadLatestReportDate(): void {
    this.isLoadingDate = true;
    this.errorMessage = '';

    this.peruAccountingReportService
      .getLatestReportDate()
      .subscribe({
        next: response => {
          this.reportDate =
            response?.bodyResponse?.reportDate ?? null;

          this.isLoadingDate = false;
        },
        error: error => {
          console.error(
            'Error consulting the latest Peru accounting report date:',
            error
          );

          this.reportDate = null;
          this.errorMessage =
            'No fue posible consultar la fecha del último reporte.';
          this.isLoadingDate = false;
        }
      });
  }

  /**
   * Ejecuta la carga de la información del reporte contable.
   */
  public generateReport(): void {
    if (this.isGenerating) {
      return;
    }

    this.isGenerating = true;
    this.errorMessage = '';

    this.peruAccountingReportService
      .generateReport()
      .subscribe({
        next: response => {
          const message =
            response?.bodyResponse ||
            'Información generada correctamente.';

          this.toastr.success(message);
          this.isGenerating = false;
          this.loadLatestReportDate();
        },
        error: error => {
          console.error(
            'Error generating the Peru accounting report:',
            error
          );

          this.errorMessage =
            'No fue posible generar la información del reporte.';
          this.toastr.error(this.errorMessage);
          this.isGenerating = false;
        }
      });
  }

  /**
   * Descarga el reporte contable en formato Excel.
   */
  public downloadReport(): void {
    if (this.isDownloading) {
      return;
    }

    this.isDownloading = true;
    this.errorMessage = '';

    this.peruAccountingReportService
      .downloadReport()
      .subscribe({
        next: response => {
          this.saveExcelFile(response);
          this.isDownloading = false;
        },
        error: error => {
          console.error(
            'Error downloading the Peru accounting report:',
            error
          );

          this.errorMessage =
            'No fue posible descargar el reporte contable.';
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
      'ReporteContablePeru.xlsx';
  }
}
