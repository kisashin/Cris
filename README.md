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
import { DateFormatService } from '../../../../shared/services/date-format.service';
import { ConfirmDialogComponent } from '../../components/confirm-dialog/confirm-dialog.component';
import { IColombiaXmlFile } from '../../models/colombia-accounting-result.model';

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
  public isLoading = false;
  public isLoadingReport = false;
  public hasAvalData = false;

  public dataSource: IColombiaXmlFile[] = [];
  public dataSourceAval: any[] = [];

  public readonly displayedColumns: string[] = [
    'processDate',
    'period',
    'family',
    'movementType',
    'lineCount',
    'status',
    'action'
  ];

  public readonly displayedColumnsAval: string[] = [
    'dateGenerate',
    'status',
    'nombreRpt',
    'actions'
  ];

  constructor(
    private readonly avalService: ClosingAvalService,
    private readonly dateFmt: DateFormatService,
    private readonly dialog: MatDialog,
    private readonly toastr: ToastrService
  ) {}

  ngOnInit(): void {
    this.loadAvalReports();
    this.loadGeneratedFiles();
  }

  /**
   * Consulta el estado del reporte mensual de Aval.
   */
  public loadAvalReports(): void {
    this.isLoadingReport = true;
    this.avalService.getAllReportsDetailsAval().subscribe({
      next: details => {
        if (!details || details.length === 0) {
          this.hasAvalData = false;
          this.dataSourceAval = [];
          this.isLoadingReport = false;
          return;
        }

        this.hasAvalData = true;
        this.dataSourceAval = details.map(d => ({
          dateGenerate: this.dateFmt.formatDate(d.dateGenerate),
          status: d.status,
          nombreRpt: d.nombreRpt
        }));
        this.isLoadingReport = false;
      },
      error: error => {
        console.error('Error al obtener reportes ', error);
        this.hasAvalData = false;
        this.isLoadingReport = false;
      }
    });
  }

  /**
   * Solicita la generacion del reporte mensual de Aval.
   */
  public generateAval(): void {
    this.isLoadingReport = true;
    this.avalService.updateReportsAval().subscribe({
      next: () => this.loadAvalReports(),
      error: error => {
        console.error('Error al actualizar reporte Aval', error);
        this.toastr.error('No fue posible generar el reporte de Aval.');
        this.isLoadingReport = false;
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
}
