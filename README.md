export interface AccountingRequest {

    product: string;
    comment: string;
}

export interface SendAccountingRequest {

    product: string;
    comment: string;
    user: string;
}

export interface LoadResult {

    message: string;
    totalRows: number;
    incompleteRows: number;
}

export interface AccountingFile {

    id: number;
    product: string;
    journalType: string;
    fileName: string;
    generationDate: string;
}
