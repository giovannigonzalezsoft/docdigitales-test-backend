from fastapi import APIRouter, Depends, status

from app.modules.invoices.deps import get_invoice_service
from app.modules.invoices.schemas import OverdueInvoiceResponse
from app.modules.invoices.service import InvoiceService


router = APIRouter(
    prefix="/invoices",
    tags=["Invoices"],
)


@router.get(
    "/overdue",
    response_model=list[OverdueInvoiceResponse],
    status_code=status.HTTP_200_OK,
)
async def get_overdue_invoices(
    service: InvoiceService = Depends(get_invoice_service),
) -> list[OverdueInvoiceResponse]:
    """
    Descripcion:
        Obtiene todas las facturas vencidas con saldo pendiente de pago.

    Response:
        list[OverdueInvoiceResponse]
    """

    return await service.get_overdue_with_pending_balance()
