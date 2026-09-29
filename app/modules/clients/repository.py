from sqlalchemy import RowMapping, Sequence, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.clients.models import Client
from app.modules.invoices.models import Invoice
from app.modules.payments.models import Payment


class ClientRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_billing_summary(self) -> Sequence[RowMapping]:
        payments_subquery = (
            select(
                Payment.invoice_id,
                func.sum(Payment.amount).label("total_paid"),
            )
            .group_by(Payment.invoice_id)
            .subquery()
        )

        query = (
            select(
                Client.id.label("client_id"),
                Client.name.label("client_name"),
                func.coalesce(
                    func.sum(Invoice.total),
                    0,
                ).label("total_invoiced"),
                func.coalesce(
                    func.sum(payments_subquery.c.total_paid),
                    0,
                ).label("total_paid"),
            )
            .outerjoin(
                Invoice,
                Invoice.client_id == Client.id,
            )
            .outerjoin(
                payments_subquery,
                payments_subquery.c.invoice_id == Invoice.id,
            )
            .group_by(
                Client.id,
                Client.name,
            )
            .order_by(Client.id)
        )

        result = await self.session.execute(query)

        return result.mappings().all()
