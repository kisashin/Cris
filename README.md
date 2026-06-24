src/app/views/claims-closing/movements-peru/cardif-peru-closing/cardif-peru-closing.component.scss
src/app/views/claims-closing/movements-peru/cardif-peru-closing/cardif-peru-closing.component.spec.ts



src/app/views/claims-closing/services/cardif-peru-closing.service.ts
src/app/views/claims-closing/services/cardif-peru-closing.service.spec.ts

.accounting-report-container {
  width: 100%;
  max-width: 900px;
  padding: 1rem 0;
}

.container-title {
  padding-bottom: 3rem;

  .title {
    margin: 0;
    color: #006600;
    font-family: 'Franklin Gothic Medium', Arial, sans-serif;
    font-size: 14pt;
    font-weight: 600;
  }
}

.action-section {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.section-label {
  color: #006600;
  font-family: 'Franklin Gothic Medium', Arial, sans-serif;
  font-weight: 600;
  font-size: 14px;
}

.action-button,
.download-button {
  min-height: 40px;
  padding: 0 1.25rem;
  color: #ffffff !important;
  background-color: #006600 !important;
  font-family: 'Franklin Gothic Medium', Arial, sans-serif;
  font-weight: 500;
  text-transform: uppercase;

  mat-icon {
    margin-right: 6px;
  }

  &:hover:not(:disabled) {
    background-color: #004d00 !important;
  }

  &:disabled {
    color: rgba(255, 255, 255, 0.7) !important;
    background-color: #7aa87a !important;
    cursor: not-allowed;
  }
}

.error-message {
  width: 100%;
  max-width: 700px;
  margin: 0 0 1.5rem;
  padding: 0.75rem 1rem;
  color: #a40000;
  background-color: #fdeaea;
  border: 1px solid #d60000;
  border-radius: 4px;
  font-size: 13px;
}

@media (max-width: 768px) {
  .accounting-report-container {
    padding: 1rem;
  }

  .container-title {
    padding-bottom: 2rem;
  }

  .action-section {
    align-items: flex-start;
    flex-direction: column;
    gap: 1rem;
  }

  .action-button,
  .download-button {
    width: 100%;
  }
}
