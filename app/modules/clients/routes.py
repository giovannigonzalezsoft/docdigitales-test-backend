from fastapi import APIRouter, Depends, status

from app.modules.clients.deps import get_client_service
from app.modules.clients.schemas import ClientBillingSummaryResponse
from app.modules.clients.service import ClientService


router = APIRouter(
    prefix="/clients",
    tags=["Clients"],
)


@router.get(
    "/billing-summary",
    response_model=list[ClientBillingSummaryResponse],
    status_code=status.HTTP_200_OK,
)
async def get_billing_summary(
    service: ClientService = Depends(get_client_service),
) -> list[ClientBillingSummaryResponse]:
    """
    Descripcion:
        Obtiene un resumen de facturación para cada cliente. 
        Incluye el total facturado y el total pagado.

    Response:
        list[ClientBillingSummaryResponse]
    """

    return await service.get_billing_summary()
