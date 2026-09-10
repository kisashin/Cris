import { IAvalReportFile } from '../../models/aval-report-status.model';

  public isGeneratingReport = false;
  public isDownloadingReport = false;
  public reportDataSource: IAvalReportFile[] = [];

  public readonly displayedColumnsReport: string[] = [
    'processDate',
    'reportStatus',
    'actions',
    'action'
  ];


  /**
   * Consulta el estado del reporte mensual de Aval.
   */
  public loadReportStatus(): void {
    this.isLoadingReport = true;
    this.avalService
      .findReportStatus()
      .subscribe({
        next: response => {
          const status = response?.bodyResponse;
          this.reportDataSource = status ? [status] : [];
          this.isLoadingReport = false;
        },
        error: error => {
          console.error('Error loading the Aval report status:', error);
          this.reportDataSource = [];
          this.isLoadingReport = false;
        }
      });
  }

  /**
   * Devuelve el mensaje de estado de la grilla del reporte.
   */
  public getReportStatusLabel(row: IAvalReportFile): string {
    return (row?.pendingMovements ?? 0) > 0
      ? 'Registros nuevos listos para generar'
      : 'No registros para consultar';
  }

  /**
   * Solicita confirmacion antes de generar el reporte.
   */
  public generateReport(row: IAvalReportFile): void {
    if (this.isGeneratingReport) {
      return;
    }

    const hasPending = (row?.pendingMovements ?? 0) > 0;

    this.dialog
      .open(ConfirmDialogComponent, {
        width: '440px',
        disableClose: true,
        data: {
          title: 'Generar reporte de movimientos',
          message: hasPending
            ? '¿Seguro que quiere generar el reporte? Se reemplazará el '
              + 'archivo generado anteriormente.'
            : 'No existen movimientos pendientes por reportar. Si continúa, '
              + 'el reporte se generará vacío y reemplazará al anterior.',
          confirmText: 'SÍ, GENERAR',
          cancelText: 'NO'
        }
      })
      .afterClosed()
      .subscribe(confirmed => {
        if (confirmed) {
          this.executeReportGeneration();
        }
      });
  }

  /**
   * Descarga el reporte mensual de Aval.
   */
  public downloadReport(row: IAvalReportFile): void {
    if (this.isDownloadingReport || !row?.id) {
      return;
    }

    this.isDownloadingReport = true;
    this.avalService
      .downloadAvalReport(row.id)
      .subscribe({
        next: response => {
          this.saveBlobFile(response, row.fileName);
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

  private executeReportGeneration(): void {
    this.isGeneratingReport = true;
    this.avalService
      .generateAvalReport()
      .subscribe({
        next: () => {
          this.toastr.success('Reporte generado correctamente.');
          this.isGeneratingReport = false;
          this.loadReportStatus();
        },
        error: error => {
          console.error('Error generating the Aval report:', error);
          this.toastr.error(
            error?.error?.errorHeader?.errorMessage ??
            'No fue posible generar el reporte de movimientos.'
          );
          this.isGeneratingReport = false;
          this.loadReportStatus();
        }
      });
  }
  
