export interface IAccountingXmlFile {
  movementType: string;
  fileName: string;
  lineCount: number;
  content: string;
}

export interface ICenterAccountingResult {
  message: string;
  processDate: string;
  status: string;
  period: string;
  files: IAccountingXmlFile[];
}
