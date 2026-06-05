private formatDate(date: any): string | null {
  if (!date) return null;
  const d = new Date(date);
  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

fechaInicio: this.formatDate(formValue.startDate),
fechaFin: this.formatDate(formValue.endDate)
