onSearch(): void {
  if (this.productForm.valid) {
    const producto = Number(this.productForm.value.product);
    this.homologationPolicyAlfaSrv.buscarPorProducto(producto).subscribe({
      next: (response) => {
        if (response && response.bodyResponse) {
          this.dataSource = response.bodyResponse.map((item: any) => ({
            id: item.id,
            productCode: item.producto,
            ramoCode: item.ramo,
            policyNumber: item.nroPoliza,
            aplicaVigencia: item.aplicaVigencia,
            startDate: item.fechaInicio,
            endDate: item.fechaFin
          }));
        }
      },
      error: (error) => {
        console.error('Error al buscar homologaciones:', error);
      }
    });
  }
}

const payload: any = {
  producto: Number(formValue.productCode),
  ramo: Number(formValue.ramoCode),
  nroPoliza: formValue.policyNumber,
  aplicaVigencia: formValue.appliesValidity.value === 'si' ? 1 : 0,
  fechaInicio: formValue.startDate || null,
  fechaFin: formValue.endDate || null
};
