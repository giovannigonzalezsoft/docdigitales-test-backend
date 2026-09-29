from fastapi import APIRouter

from app.modules.clients.routes import router as clients_router
from app.modules.invoices.routes import router as invoices_router
from app.modules.timbrados.routes import router as timbrados_router


api_router = APIRouter(prefix="/v1")

api_router.include_router(timbrados_router)
api_router.include_router(clients_router)
api_router.include_router(invoices_router)
