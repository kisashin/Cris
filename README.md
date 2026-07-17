registerAccountingEntry(): void {
  this.loading = true;
  this.accountingEntryService
    .registerAccountingEntry({ product: this.selectedProduct, comment: this.comment })
    .subscribe({
      next: () => {
        this.loading = false;
        this.sendMessage = 'Asiento registrado';   // <- texto fijo, NO leer del response
      },
      error: () => { this.loading = false; }
    });
}
