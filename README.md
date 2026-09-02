  private showError(error: any, fallback: string): void {

    const body = error?.error?.body ?? error?.error;

    this.toastr.error(
      body?.errorDetail?.message ?? fallback
    );

  }



          next: response => {

          this.loading = false;

          this.sendMessage = response.bodyResponse.message;

          this.toastr.success(response.bodyResponse.message);

          this.dataSource = [];

          this.loadFiles();

        },







                ToastrModule.forRoot({ closeButton: true, progressBar: true, positionClass: 'toast-top-right' }),
