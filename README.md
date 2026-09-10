export interface IAvalReportFile {
  id: number;
  period: string;
  fileName: string;
  rowCount: number;
  processDate: string;
  status: string;
  pendingMovements: number;
}
