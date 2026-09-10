        error: error => {
          console.error('Error loading the Aval report status:', error);
          this.reportDataSource = [
            { pendingMovements: 0 } as IAvalReportFile
          ];
          this.isLoadingReport = false;
        }


          this.reportDataSource = [
            status ?? ({ pendingMovements: 0 } as IAvalReportFile)
          ];        
