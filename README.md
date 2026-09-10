import { IAvalReportFile } from '../../models/aval-report-status.model';



  const reportFile: IAvalReportFile = {
    id: 1,
    period: '202609',
    fileName: 'RPT_CIERRE_AVAL.xlsx',
    rowCount: 257,
    processDate: '09/09/2026 10:00:00 a. m.',
    status: 'GENERADO',
    pendingMovements: 93
  };



      avalService = jasmine.createSpyObj('ClosingAvalService', [
      'findReportStatus',
      'generateAvalReport',
      'downloadAvalReport',
      'findGeneratedFiles',
      'generateAccountingEntries',
      'downloadXmlFile'
    ]);


        avalService.findReportStatus.and.returnValue(
      of({ bodyResponse: reportFile } as any));




  describe('#loadReportStatus', () => {
    it('should load the report status on init', () => {
      expect(component.reportDataSource.length).toBe(1);
      expect(component.reportDataSource[0].pendingMovements).toBe(93);
      expect(component.isLoadingReport).toBeFalse();
    });

    it('should use an empty list when the body is null', () => {
      avalService.findReportStatus.and.returnValue(
        of({ bodyResponse: null } as any));

      component.loadReportStatus();

      expect(component.reportDataSource).toEqual([]);
    });

    it('should clear the list when the request fails', () => {
      avalService.findReportStatus.and.returnValue(
        throwError(() => new Error('boom')));

      component.loadReportStatus();

      expect(component.reportDataSource).toEqual([]);
      expect(component.isLoadingReport).toBeFalse();
    });
  });

  describe('#getReportStatusLabel', () => {
    it('should show the pending message when there are movements', () => {
      expect(component.getReportStatusLabel(reportFile))
        .toBe('Registros nuevos listos para generar');
    });

    it('should show the empty message when there are none', () => {
      expect(component.getReportStatusLabel(
        { ...reportFile, pendingMovements: 0 }))
        .toBe('No registros para consultar');
    });

    it('should show the empty message when the row is undefined', () => {
      expect(component.getReportStatusLabel(undefined as any))
        .toBe('No registros para consultar');
    });
  });

  describe('#generateReport', () => {
    it('should generate when the dialog is confirmed', () => {
      dialog.open.and.returnValue({ afterClosed: () => of(true) } as any);
      avalService.generateAvalReport.and.returnValue(
        of({ bodyResponse: reportFile } as any));

      component.generateReport(reportFile);

      expect(avalService.generateAvalReport).toHaveBeenCalled();
      expect(toastr.success)
        .toHaveBeenCalledWith('Reporte generado correctamente.');
      expect(component.isGeneratingReport).toBeFalse();
    });

    it('should warn in the dialog when there are no pending movements', () => {
      dialog.open.and.returnValue({ afterClosed: () => of(false) } as any);

      component.generateReport({ ...reportFile, pendingMovements: 0 });

      const config = dialog.open.calls.mostRecent().args[1] as any;
      expect(config.data.message).toContain('vacío');
    });

    it('should not generate when the dialog is cancelled', () => {
      dialog.open.and.returnValue({ afterClosed: () => of(false) } as any);

      component.generateReport(reportFile);

      expect(avalService.generateAvalReport).not.toHaveBeenCalled();
    });

    it('should ignore the click while a generation is running', () => {
      component.isGeneratingReport = true;

      component.generateReport(reportFile);

      expect(dialog.open).not.toHaveBeenCalled();
    });

    it('should show the backend error message', () => {
      dialog.open.and.returnValue({ afterClosed: () => of(true) } as any);
      avalService.generateAvalReport.and.returnValue(throwError(() => ({
        error: { errorHeader: { errorMessage: 'Error controlado' } }
      })));

      component.generateReport(reportFile);

      expect(toastr.error).toHaveBeenCalledWith('Error controlado');
      expect(component.isGeneratingReport).toBeFalse();
    });

    it('should show a default error message', () => {
      dialog.open.and.returnValue({ afterClosed: () => of(true) } as any);
      avalService.generateAvalReport.and.returnValue(
        throwError(() => new Error('boom')));

      component.generateReport(reportFile);

      expect(toastr.error).toHaveBeenCalledWith(
        'No fue posible generar el reporte de movimientos.');
    });
  });

  describe('#downloadReport', () => {
    it('should download the Excel report', () => {
      avalService.downloadAvalReport.and.returnValue(of(new HttpResponse({
        body: new Blob(['excel']),
        status: 200
      })));

      const anchor = document.createElement('a');
      spyOn(document, 'createElement').and.returnValue(anchor);
      spyOn(anchor, 'click');
      spyOn(window.URL, 'createObjectURL').and.returnValue('blob:url');
      spyOn(window.URL, 'revokeObjectURL');

      component.downloadReport(reportFile);

      expect(avalService.downloadAvalReport).toHaveBeenCalledWith(1);
      expect(anchor.download).toBe('RPT_CIERRE_AVAL.xlsx');
      expect(component.isDownloadingReport).toBeFalse();
    });

    it('should ignore the click while a download is running', () => {
      component.isDownloadingReport = true;

      component.downloadReport(reportFile);

      expect(avalService.downloadAvalReport).not.toHaveBeenCalled();
    });

    it('should ignore the click when there is no report', () => {
      component.downloadReport({ ...reportFile, id: undefined as any });

      expect(avalService.downloadAvalReport).not.toHaveBeenCalled();
    });

    it('should show the backend error message', () => {
      avalService.downloadAvalReport.and.returnValue(throwError(() => ({
        error: { errorHeader: { errorMessage: 'Sin reporte' } }
      })));

      component.downloadReport(reportFile);

      expect(toastr.error).toHaveBeenCalledWith('Sin reporte');
      expect(component.isDownloadingReport).toBeFalse();
    });

    it('should show a default error message', () => {
      avalService.downloadAvalReport.and.returnValue(
        throwError(() => new Error('boom')));

      component.downloadReport(reportFile);

      expect(toastr.error).toHaveBeenCalledWith(
        'No fue posible descargar el reporte de movimientos.');
    });
  });      
