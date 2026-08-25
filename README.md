BEGIN TRAN;
EXEC dbo.sp_contabiliza_cardifCentro;
ROLLBACK;
