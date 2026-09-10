    it('should keep a placeholder row when the body is null', () => {
      avalService.findReportStatus.and.returnValue(
        of({ bodyResponse: null } as any));

      component.loadReportStatus();

      expect(component.reportDataSource.length).toBe(1);
      expect(component.reportDataSource[0].pendingMovements).toBe(0);
      expect(component.reportDataSource[0].id).toBeUndefined();
    });

    it('should keep a placeholder row when the request fails', () => {
      avalService.findReportStatus.and.returnValue(
        throwError(() => new Error('boom')));

      component.loadReportStatus();

      expect(component.reportDataSource.length).toBe(1);
      expect(component.reportDataSource[0].pendingMovements).toBe(0);
      expect(component.isLoadingReport).toBeFalse();
    });
