export interface IAccountingXmlFile {
  id: number;
  period: string;
  movementType: string;
  fileName: string;
  lineCount: number;
  processDate: string;
  status: string;
}

export interface ICenterAccountingResult {
  message: string;
  period: string;
  files: IAccountingXmlFile[];
}
