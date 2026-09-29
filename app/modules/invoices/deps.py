from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.modules.invoices.repository import InvoiceRepository
from app.modules.invoices.service import InvoiceService


def get_invoice_service(
    session: AsyncSession = Depends(get_session),
) -> InvoiceService:
    """
    Description:
        Provides an instance of the InvoiceService class.

    Returns:
        InvoiceService instance.
    """
    
    repository = InvoiceRepository(session)

    return InvoiceService(
        repository=repository,
    )
