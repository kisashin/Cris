.container-table {
  overflow-x: auto;
  padding-top: 0.5rem;

  table {
    width: 100%;
  }

  th.mat-mdc-header-cell,
  th.mat-header-cell {
    background-color: #14532d !important;
    color: #ffffff !important;
    font-family: 'Franklin Gothic Medium', Arial, sans-serif;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.03rem;
    padding: 0.9rem 0.75rem;
    text-align: center;
  }

  td.mat-mdc-cell,
  td.mat-cell {
    border-bottom: 1px solid #e0e0e0;
    font-family: Arial, sans-serif;
    font-size: 13px;
    padding: 0.75rem;
    text-align: center;
  }

  .download-link {
    color: #1976d2 !important;
    cursor: pointer;
    font-family: Arial, sans-serif;
    text-decoration: underline;

    &:hover {
      color: #0d47a1 !important;
    }
  }
}
