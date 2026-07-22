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
