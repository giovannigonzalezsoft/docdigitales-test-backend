from sqlalchemy import RowMapping, Sequence, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.invoices.models import Invoice
from app.modules.payments.models import Payment


class InvoiceRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(
    self,
    invoice_id: int,
    ) -> Invoice | None:
        """
        Description:
            Gets an invoice by id.

        Returns:
            Invoice or None.
        """

        statement = select(Invoice).where(
            Invoice.id == invoice_id
        )

        result = await self.session.execute(statement)

        return result.scalar_one_or_none()

    async def get_overdue_with_pending_balance(self) -> Sequence[RowMapping]:
        total_paid = func.coalesce(
            func.sum(Payment.amount),
            0,
        )

        pending_balance = Invoice.total - total_paid

        query = (
            select(
                Invoice.id.label("invoice_id"),
                Invoice.folio,
                Invoice.client_id,
                pending_balance.label("pending_balance"),
            )
            .outerjoin(
                Payment,
                Payment.invoice_id == Invoice.id,
            )
            .where(
                Invoice.status == "vencida",
            )
            .group_by(
                Invoice.id,
                Invoice.folio,
                Invoice.client_id,
                Invoice.total,
            )
            .having(
                pending_balance > 0,
            )
            .order_by(Invoice.id)
        )

        result = await self.session.execute(query)

        return result.mappings().all()
