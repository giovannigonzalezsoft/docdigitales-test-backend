from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.invoices.models import Invoice
from app.modules.timbrados.models import Timbrado


class TimbradoRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_external_id(
        self,
        external_id: str,
    ) -> Timbrado | None:
        """
        Description:
            Gets a stamping request by external_id.

        Returns:
            Timbrado or None.
        """

        statement = select(Timbrado).where(
            Timbrado.external_id == external_id
        )

        result = await self.session.execute(statement)

        return result.scalar_one_or_none()

    async def create(
        self,
        timbrado: Timbrado,
    ) -> Timbrado:
        """
        Description:
            Persists a new stamping request.

        Returns:
            Created Timbrado.
        """

        self.session.add(timbrado)

        await self.session.commit()
        await self.session.refresh(timbrado)

        return timbrado
