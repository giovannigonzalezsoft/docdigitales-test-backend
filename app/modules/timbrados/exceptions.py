from fastapi import HTTPException, status


class InvoiceNotFoundException(HTTPException):
    def __init__(self, invoice_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Factura con id {invoice_id} no fue encontrada.",
        )
