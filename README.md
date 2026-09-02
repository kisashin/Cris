import { Component, OnInit } from '@angular/core';
import { HttpResponse } from '@angular/common/http';
import { MatDialog } from '@angular/material/dialog';
import { ToastrService } from 'ngx-toastr';

import { IMetaColumn } from '../../models/IMetaColumn.models';
import { AccountingEntryService } from '../services/accounting-entry.service';
import { AccountingProduct } from '../models/accounting-product.model';
import { AccountingFile } from '../models/accounting-request.model';
import { ConfirmDialogComponent } from '../../components/confirm-dialog/confirm-dialog.component';

@Component({
  selector: 'app-accounting-entry',
  standalone: false,
  templateUrl: './accounting-entry.component.html',
  styleUrl: './accounting-entry.component.scss'
})
export class AccountingEntryComponent implements OnInit {

  loading = false;

  accountingDate = '';

  message = '';

  sendMessage = '';

  comment = '';

  selectedProduct!: string;

  selectedFile: File | null = null;

  products: AccountingProduct[] = [];

  files: AccountingFile[] = [];

  readonly fileColumns: string[] = [
    'product',
    'journalType',
    'fileName',
    'generationDate',
    'action'
  ];

  dataSource: any[] = [];

  generateColumns: IMetaColumn[] = [
    { title: 'Tipo', field: 'journalType' },
    { title: 'Cuenta', field: 'accountCode' },
    { title: 'Referencia', field: 'transactionReference' },
    { title: 'Descripción', field: 'description' },
    { title: 'D/C', field: 'debitCredit' },
    { title: 'Importe', field: 'transactionAmount' }
  ];

  totalColumns: IMetaColumn[] = [
    { title: 'Producto', field: 'product' },
    { title: 'Tipo', field: 'journalType' },
    { title: 'Referencia', field: 'transactionReference' },
    { title: 'Cuenta', field: 'accountCode' },
    { title: 'Débito', field: 'debit' },
    { title: 'Crédito', field: 'credit' }
  ];

  displayedColumns: IMetaColumn[] = this.totalColumns;

  constructor(
    private accountingEntryService: AccountingEntryService,
    private dialog: MatDialog,
    private toastr: ToastrService
  ) { }

  ngOnInit(): void {

    this.loadAccountingDate();

    this.loadProducts();

    this.loadFiles();

  }

  loadAccountingDate(): void {

    this.accountingEntryService
      .getAccountingDate()
      .subscribe(response => {

        this.accountingDate = response.bodyResponse.accountingDate;

      });

  }

  loadProducts(): void {

    this.accountingEntryService
      .getProducts()
      .subscribe(response => {

        this.products = response.bodyResponse;

        if (this.products.length > 0) {

          this.selectedProduct = this.products[0].product;

          this.buildComment();

        }

      });

  }

  /**
   * Archivos generados del periodo contable actual.
   */
  loadFiles(): void {

    this.accountingEntryService
      .getFiles()
      .subscribe({

        next: response => {

          this.files = response?.bodyResponse ?? [];

        },

        error: () => {

          this.files = [];

        }

      });

  }

  onProductChange(): void {

    this.buildComment();

    this.dataSource = [];

    this.sendMessage = '';

    this.message = '';

    this.selectedFile = null;

  }

  /**
   * Guarda el archivo seleccionado en el explorador.
   */
  onFileSelected(event: Event): void {

    const input = event.target as HTMLInputElement;

    this.selectedFile = input.files?.length ? input.files[0] : null;

    this.message = '';

  }

  private buildComment(): void {

    if (!this.accountingDate || !this.selectedProduct) {

      return;

    }

    const period = this.accountingDate.substring(0, 6);

    this.comment = `${this.selectedProduct}_${period}`;

  }

  loadClaims(): void {

    if (!this.selectedProduct) {

      this.toastr.warning('Debe seleccionar un producto.');

      return;

    }

    if (!this.selectedFile) {

      this.toastr.warning('Debe seleccionar un archivo.');

      return;

    }

    this.loading = true;

    this.accountingEntryService
      .loadClaims(this.selectedFile, this.selectedProduct, this.getUser())
      .subscribe({

        next: response => {

          this.loading = false;

          const result = response.bodyResponse;

          this.message = result.message;

          if (result.incompleteRows > 0) {

            this.toastr.warning(
              `${result.incompleteRows} de ${result.totalRows} filas venían incompletas.`
            );

          }

          this.dataSource = [];

        },

        error: error => {

          this.loading = false;

          this.showError(error, 'No fue posible cargar el archivo.');

        }

      });

  }

  generateAccountingEntry(): void {

    this.loading = true;

    this.accountingEntryService
      .previewAccountingEntry({

        product: this.selectedProduct,

        comment: this.comment

      })
      .subscribe({

        next: response => {

          this.loading = false;

          this.displayedColumns = this.generateColumns;

          this.dataSource = this.roundAmounts(response.bodyResponse);

        },

        error: error => {

          this.loading = false;

          this.showError(error, 'No fue posible generar el asiento.');

        }

      });

  }

  /**
   * El back /register devuelve cuerpo null: NO se lee del response, texto fijo.
   */
  registerAccountingEntry(): void {

    this.loading = true;

    this.accountingEntryService
      .registerAccountingEntry({

        product: this.selectedProduct,

        comment: this.comment

      })
      .subscribe({

        next: () => {

          this.loading = false;

          this.sendMessage = 'Asiento registrado';

        },

        error: error => {

          this.loading = false;

          this.showError(error, 'No fue posible registrar el asiento.');

        }

      });

  }

  getAccountSummary(): void {

    this.loading = true;

    this.accountingEntryService
      .getAccountSummary({

        product: this.selectedProduct,

        comment: this.comment

      })
      .subscribe({

        next: response => {

          this.loading = false;

          this.displayedColumns = this.totalColumns;

          this.dataSource = this.roundAmounts(response.bodyResponse);

        },

        error: error => {

          this.loading = false;

          this.showError(error, 'No fue posible consultar el total por cuenta.');

        }

      });

  }

  /**
   * Pide confirmacion antes de generar, porque los archivos previos del
   * producto se reemplazan.
   */
  sendAccountingEntry(): void {

    if (this.loading) {

      return;

    }

    this.dialog
      .open(ConfirmDialogComponent, {
        width: '440px',
        disableClose: true,
        data: {
          title: 'Generar XML',
          message: `¿Seguro que quiere generar el XML del producto `
            + `${this.selectedProduct}? Los archivos anteriores de este `
            + `producto se reemplazarán.`,
          confirmText: 'SÍ, GENERAR',
          cancelText: 'NO'
        }
      })
      .afterClosed()
      .subscribe(confirmed => {

        if (confirmed) {

          this.executeSend();

        }

      });

  }

  private executeSend(): void {

    this.loading = true;

    this.accountingEntryService
      .sendAccountingEntry({

        product: this.selectedProduct,

        comment: this.comment,

        user: this.getUser()

      })
      .subscribe({

        next: response => {

          this.loading = false;

          this.sendMessage = response.bodyResponse.message;

          this.loadFiles();

        },

        error: error => {

          this.loading = false;

          this.showError(error, 'No fue posible generar los asientos contables.');

        }

      });

  }

  /**
   * Descarga el XML de la fila seleccionada.
   */
  onDownloadXml(row: AccountingFile): void {

    this.accountingEntryService
      .downloadFile(row.id)
      .subscribe({

        next: response => this.saveBlobFile(response, row.fileName),

        error: error => {

          this.showError(error, 'No fue posible descargar el archivo XML.');

        }

      });

  }

  private saveBlobFile(response: HttpResponse<Blob>, fileName: string): void {

    const file = response.body;

    if (!file || file.size === 0) {

      this.toastr.warning('El archivo generado no contiene información.');

      return;

    }

    const objectUrl = window.URL.createObjectURL(file);

    const anchor = document.createElement('a');

    anchor.href = objectUrl;

    anchor.download = fileName;

    anchor.click();

    window.URL.revokeObjectURL(objectUrl);

  }

  private showError(error: any, fallback: string): void {

    this.toastr.error(
      error?.error?.errorDetail?.message ?? fallback
    );

  }

  private getUser(): string {

    return sessionStorage.getItem('user') ?? '';

  }

  private roundAmounts(rows: any[]): any[] {
    return rows.map(row => {
      const rounded: any = { ...row };
      Object.keys(rounded).forEach(key => {
        if (typeof rounded[key] === 'number') {
          rounded[key] = Math.round(rounded[key] * 100) / 100;
        }
      });
      return rounded;
    });
  }

}
