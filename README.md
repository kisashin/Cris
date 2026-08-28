import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { HttpResponse } from '@angular/common/http';
import { MatButtonModule } from '@angular/material/button';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { MatTableModule } from '@angular/material/table';
import { MatIconModule } from '@angular/material/icon';
import { ToastrService } from 'ngx-toastr';
import { environment } from 'src/environments/environment';
import { ClosingAvalService } from '../../services/closing-aval.service';
import { ConfirmDialogComponent } from '../../components/confirm-dialog/confirm-dialog.component';
import { IColombiaXmlFile } from '../../models/colombia-accounting-result.model';
import { IAvalReportStatus } from '../../models/aval-report-status.model';

/**
 * Pantalla Cierre Mensual de Aval.
 */
@Component({
  selector: 'app-claims-closing-aval',
  imports: [
    CommonModule,
    MatTableModule,
    MatButtonModule,
    MatIconModule,
    MatDialogModule
  ],
  standalone: true,
  templateUrl: './claims-closing-aval.component.html',
  styleUrl: './claims-closing-aval.component.scss'
})
export class ClaimsClosingAvalComponent implements OnInit {

  readonly reportMovement = `${environment.reporting_service}/ReportServer/Pages/ReportViewer.aspx?/Acsele/Alterno/Cierre_siniestrosaval&rs:Command=Render&rc:Parameters=false&rc:Toolbar=false&rs:Format=Excel`;

  public isGenerating = false;
  public isDownloadingReport = false;
  public isLoading = false;
  public isLoadingReport = false;
  public hasAvalData = false;

  public dataSource: IColombiaXmlFile[] = [];
  public reportDataSource: IAvalReportStatus[] = [];

  public readonly displayedColumns: string[] = [
    'processDate',
    'period',
    'family',
    'movementType',
    'lineCount',
    'status',
    'action'
  ];

  public readonly displayedColumnsReport: string[] = [
    'generationDate',
    'action'
  ];

  constructor(
    private readonly avalService: ClosingAvalService,
    private readonly dialog: MatDialog,
    private readonly toastr: ToastrService
  ) {}

  ngOnInit(): void {
    this.loadReportStatus();
    this.loadGeneratedFiles();
  }

  /**
   * Consulta si existen movimientos pendientes por reportar.
   */
  public loadReportStatus(): void {
    this.isLoadingReport = true;
    this.avalService
      .findReportStatus()
      .subscribe({
        next: response => {
          const status = response?.bodyResponse;
          this.hasAvalData = (status?.pendingMovements ?? 0) > 0;
          this.reportDataSource = this.hasAvalData && status
            ? [status]
            : [];
          this.isLoadingReport = false;
        },
        error: error => {
          console.error('Error loading the Aval report status:', error);
          this.hasAvalData = false;
          this.reportDataSource = [];
          this.isLoadingReport = false;
        }
      });
  }

  /**
   * Descarga el reporte mensual de Aval.
   */
  public downloadReport(): void {
    if (this.isDownloadingReport) {
      return;
    }

    this.isDownloadingReport = true;
    this.avalService
      .downloadAvalReport()
      .subscribe({
        next: response => {
          this.saveBlobFile(response, this.getFileName(response));
          this.isDownloadingReport = false;
        },
        error: error => {
          console.error('Error downloading the Aval report:', error);
          this.toastr.error(
            error?.error?.errorHeader?.errorMessage ??
            'No fue posible descargar el reporte de movimientos.'
          );
          this.isDownloadingReport = false;
        }
      });
  }

  /**
   * Consulta los archivos generados en procesos anteriores.
   */
  public loadGeneratedFiles(): void {
    this.isLoading = true;
    this.avalService
      .findGeneratedFiles()
      .subscribe({
        next: response => {
          this.dataSource = response?.bodyResponse ?? [];
          this.isLoading = false;
        },
        error: error => {
          console.error('Error loading Aval accounting files:', error);
          this.dataSource = [];
          this.isLoading = false;
        }
      });
  }

  /**
   * Solicita confirmacion antes de generar los asientos contables.
   */
  public generateAccountingEntries(): void {
    if (this.isGenerating) {
      return;
    }

    this.dialog
      .open(ConfirmDialogComponent, {
        width: '440px',
        disableClose: true,
        data: {
          title: 'Generar nuevo XML',
          message: '¿Seguro que quiere generar un nuevo XML? Al hacerlo se '
            + 'borrarán los registros anteriores.',
          confirmText: 'SÍ, GENERAR',
          cancelText: 'NO'
        }
      })
      .afterClosed()
      .subscribe(confirmed => {
        if (confirmed) {
          this.executeGeneration();
        }
      });
  }

  /**
   * Descarga el XML de la fila seleccionada.
   */
  public onDownloadXml(row: IColombiaXmlFile): void {
    this.avalService
      .downloadXmlFile(row.id)
      .subscribe({
        next: response => this.saveBlobFile(response, row.fileName),
        error: error => {
          console.error('Error downloading the XML file:', error);
          this.toastr.error('No fue posible descargar el archivo XML.');
        }
      });
  }

  private executeGeneration(): void {
    this.isGenerating = true;
    this.avalService
      .generateAccountingEntries()
      .subscribe({
        next: response => {
          this.toastr.success(
            response?.bodyResponse?.message ??
            'Proceso ejecutado correctamente.'
          );
          this.isGenerating = false;
          this.loadGeneratedFiles();
          this.loadReportStatus();
        },
        error: error => {
          console.error(
            'Error generating Aval accounting entries:',
            error
          );
          this.toastr.error(
            error?.error?.errorHeader?.errorMessage ??
            'No fue posible generar los asientos contables.'
          );
          this.isGenerating = false;
          this.loadGeneratedFiles();
          this.loadReportStatus();
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
    return fileNameMatch?.[1] ?? 'RPT_CIERRE_AVAL.xlsx';
  }
}
