import { Component, OnInit } from '@angular/core';
import { PageEvent } from '@angular/material/paginator';
import { ToastrService } from 'ngx-toastr';
import { finalize } from 'rxjs/operators';

import {
  AuxiliaryPaymentsReportStatus,
  AuxiliaryPaymentsInconsistentCoverage
} from '../../models/report-data.model';

import { ReportDataService } from '../../services/report-data.service';
import { IMetaColumn } from '../../models/IMetaColumn.models';

@Component({
  selector: 'report-data-ca',
  templateUrl: './report-data-ca.component.html',
  styleUrls: ['./report-data-ca.component.scss'],
  standalone: false
})
export class ReportDataComponent implements OnInit {

  loading = false;

  reportStatus: AuxiliaryPaymentsReportStatus[] = [];

  inconsistentCoverages: AuxiliaryPaymentsInconsistentCoverage[] = [];

  /**
   * Columnas de la tabla Estado del Reporte.
   */
  statusColumns: string[] = [
    'fechaproceso',
    'reportes'
  ];

  /**
   * Columnas de la tabla Coberturas Inconsistentes.
   */
  displayedColumnsCoverage: IMetaColumn[] = [
    {
      title: 'Llave Siniestro',
      field: 'llavesiniestros'
    }
  ];

  coveragePageIndex = 0;
  coveragePageSize = 10;
  coverageTotalElements = 0;

  pagedInconsistentCoverages: AuxiliaryPaymentsInconsistentCoverage[] = [];

  constructor(
    private readonly reportDataService: ReportDataService,
    private readonly toastr: ToastrService
  ) { }

  ngOnInit(): void {
    this.loadInformation();
  }

  loadInformation(): void {
    this.loading = true;

    this.loadStatus();
    this.loadInconsistentCoverages();
  }

  private loadStatus(): void {
    this.reportDataService
      .getReportStatus()
      .pipe(
        finalize(() => {
          this.loading = false;
        })
      )
      .subscribe({
        next: response => {
          this.reportStatus = response ?? [];
        },
        error: () => {
          this.toastr.error(
            'Error consultando estado del reporte.'
          );
        }
      });
  }

  private loadInconsistentCoverages(): void {
    this.reportDataService
      .getInconsistentCoverages()
      .subscribe({
        next: response => {
          this.inconsistentCoverages = response ?? [];
          this.coverageTotalElements =
            this.inconsistentCoverages.length;

          this.coveragePageIndex = 0;
          this.updateCoveragePage();
        },
        error: () => {
          this.inconsistentCoverages = [];
          this.coverageTotalElements = 0;
          this.pagedInconsistentCoverages = [];

          this.toastr.error(
            'Error consultando coberturas inconsistentes.'
          );
        }
      });
  }

  private updateCoveragePage(): void {
    const start =
      this.coveragePageIndex * this.coveragePageSize;

    const end =
      start + this.coveragePageSize;

    this.pagedInconsistentCoverages =
      this.inconsistentCoverages.slice(start, end);
  }

  changeCoveragePage(event: PageEvent): void {
    this.coveragePageIndex = event.pageIndex;
    this.coveragePageSize = event.pageSize;

    this.updateCoveragePage();
  }

  generateInformation(): void {
    if (this.loading) {
      return;
    }

    this.loading = true;

    this.reportDataService
      .generateInformation()
      .pipe(
        finalize(() => {
          this.loading = false;
        })
      )
      .subscribe({
        next: () => {
          this.toastr.success(
            'Información generada correctamente.'
          );

          this.loadInformation();
        },
        error: () => {
          this.toastr.error(
            'Error generando la información.'
          );
        }
      });
  }

  downloadData(): void {
    if (this.loading) {
      return;
    }

    this.loading = true;

    this.reportDataService
      .downloadDataReport()
      .pipe(
        finalize(() => {
          this.loading = false;
        })
      )
      .subscribe({
        next: response => {
          this.reportDataService.downloadFile(response);

          this.toastr.success(
            'Reporte de datos descargado correctamente.'
          );
        },
        error: () => {
          this.toastr.error(
            'Error descargando el reporte de datos.'
          );
        }
      });
  }

  downloadMovements(): void {
    if (this.loading) {
      return;
    }

    this.loading = true;

    this.reportDataService
      .downloadMovementsReport()
      .pipe(
        finalize(() => {
          this.loading = false;
        })
      )
      .subscribe({
        next: response => {
          this.reportDataService.downloadFile(response);

          this.toastr.success(
            'Reporte de movimientos descargado correctamente.'
          );
        },
        error: () => {
          this.toastr.error(
            'Error descargando el reporte de movimientos.'
          );
        }
      });
  }
}
