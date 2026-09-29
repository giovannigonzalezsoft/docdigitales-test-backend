from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.modules.clients.repository import ClientRepository
from app.modules.clients.service import ClientService


def get_client_service(
    session: AsyncSession = Depends(get_session),
) -> ClientService:
    """
    Description:
        Provides an instance of the ClientService class.

    Returns:
        ClientService instance.
    """
    repository = ClientRepository(session)

    return ClientService(
        repository=repository,
    )
