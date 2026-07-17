import { Component, OnInit } from '@angular/core';
import { IMetaColumn } from '../../claims-closing/models/IMetaColumn.models';
import { AccountingEntryService } from '../services/accounting-entry.service';
import { AccountingProduct } from '../models/accounting-product.model';

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

  products: AccountingProduct[] = [];

  // Carga dos formas distintas (modo 1 = 27 col, modo 3 = 6 col) => any[]
  dataSource: any[] = [];

  // Columnas de "Generar Asiento" (modo 1). Los field DEBEN coincidir con
  // los nombres de AccountingEntryRowDto del back.
  generateColumns: IMetaColumn[] = [
    { title: 'Tipo', field: 'journalType' },
    { title: 'Cuenta', field: 'accountCode' },
    { title: 'Referencia', field: 'transactionReference' },
    { title: 'Descripción', field: 'description' },
    { title: 'D/C', field: 'debitCredit' },
    { title: 'Importe', field: 'transactionAmount' }
  ];

  // Columnas de "Total x Cuenta" (modo 3). Coinciden con AccountTotalRowDto.
  totalColumns: IMetaColumn[] = [
    { title: 'Producto', field: 'product' },
    { title: 'Tipo', field: 'journalType' },
    { title: 'Referencia', field: 'transactionReference' },
    { title: 'Cuenta', field: 'accountCode' },
    { title: 'Débito', field: 'debit' },
    { title: 'Crédito', field: 'credit' }
  ];

  // Se cambia según el botón que se presione
  displayedColumns: IMetaColumn[] = this.totalColumns;

  constructor(
    private accountingEntryService: AccountingEntryService
  ) { }

  ngOnInit(): void {

    this.loadAccountingDate();

    this.loadProducts();

  }

  /**
   * Fecha contable
   */
  loadAccountingDate(): void {

    this.accountingEntryService
      .getAccountingDate()
      .subscribe(response => {

        this.accountingDate = response.bodyResponse.accountingDate;

      });

  }

  /**
   * Productos
   */
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
   * Cambio de producto
   */
  onProductChange(): void {

    this.buildComment();

    this.dataSource = [];

    this.sendMessage = '';

    this.message = '';

  }

  /**
   * Comentario
   */
  private buildComment(): void {

    if (!this.accountingDate || !this.selectedProduct) {

      return;

    }

    const period = this.accountingDate.substring(0, 6);

    this.comment = `${this.selectedProduct}_${period}`;

  }

  /**
   * Cargar
   */
  loadClaims(): void {

    this.loading = true;

    this.accountingEntryService
      .loadClaims({
        product: this.selectedProduct
      })
      .subscribe({

        next: response => {

          this.loading = false;

          this.message = response.bodyResponse.message;

          this.dataSource = [];

        },

        error: () => {

          this.loading = false;

        }

      });

  }

  /**
   * Generar asiento (modo 1)
   */
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

          this.dataSource = response.bodyResponse;

        },

        error: () => {

          this.loading = false;

        }

      });

  }

  /**
   * Registrar asiento
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

        error: () => {

          this.loading = false;

        }

      });

  }

  /**
   * Total por cuenta (modo 3)
   */
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

          this.dataSource = response.bodyResponse;

        },

        error: () => {

          this.loading = false;

        }

      });

  }

  /**
   * Enviar
   */
  sendAccountingEntry(): void {

    this.loading = true;

    this.accountingEntryService
      .sendAccountingEntry({

        product: this.selectedProduct,

        comment: this.comment

      })
      .subscribe({

        next: response => {

          this.loading = false;

          this.sendMessage = response.bodyResponse.message;

        },

        error: () => {

          this.loading = false;

        }

      });

  }

}
