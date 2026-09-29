from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_session
from app.modules.invoices.repository import InvoiceRepository
from app.integrations.pac_gateway import PacGateway
from app.modules.timbrados.repository import TimbradoRepository
from app.modules.timbrados.service import TimbradoService


def get_pac_gateway() -> PacGateway:
    """
    Description:
        Provides the simulated PAC gateway.

    Returns:
        PacGateway instance.
    """

    return PacGateway(
        should_fail=settings.PAC_SHOULD_FAIL
    )


async def get_timbrado_service(
    session: AsyncSession = Depends(get_session),
    pac_gateway: PacGateway = Depends(get_pac_gateway),
) -> TimbradoService:
    """
    Description:
        Provides TimbradoService with its dependencies.

    Returns:
        TimbradoService instance.
    """

    repository = TimbradoRepository(session)

    return TimbradoService(
        repository=repository,
        invoice_repository=InvoiceRepository(session),
        pac_gateway=pac_gateway,
    )
