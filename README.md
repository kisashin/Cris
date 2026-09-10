  public isGenerating = false;
  public isLoading = false;
  public isGeneratingReport = false;
  public isDownloadingReport = false;
  public isLoadingReport = false;

  public dataSource: IColombiaXmlFile[] = [];
  public reportDataSource: IAvalReportFile[] = [];

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
    'processDate',
    'reportStatus',
    'actions',
    'action'
  ];
