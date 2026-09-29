from fastapi import APIRouter, Depends, Response, status

from app.modules.timbrados.deps import get_timbrado_service
from app.modules.timbrados.schemas import (
    TimbradoCreate,
    TimbradoResponse,
)
from app.modules.timbrados.service import TimbradoService


router = APIRouter(
    prefix="/timbrados",
    tags=["Timbrados"],
)


@router.post(
    "",
    response_model=TimbradoResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_200_OK: {
            "model": TimbradoResponse,
            "description": "Request previamente procesada.",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Factura no encontrada.",
        },
        status.HTTP_422_UNPROCESSABLE_CONTENT: {
            "description": "PAC no disponible.",
        },
    },
)
async def create_timbrado(
    payload: TimbradoCreate,
    response: Response,
    service: TimbradoService = Depends(get_timbrado_service),
) -> TimbradoResponse:
    """
    Descripcion:
        Crea una solicitud de timbrado idempotente. 
        Si la solicitud ya fue procesada, devuelve el resultado previo.

    Response:
        TimbradoResponse
    """

    result, created = await service.create(payload)

    if not created:
        response.status_code = status.HTTP_200_OK
    elif result.status == "fallida":
        response.status_code = status.HTTP_422_UNPROCESSABLE_CONTENT

    return result
