from app.modules.invoices.repository import InvoiceRepository
from app.modules.invoices.schemas import OverdueInvoiceResponse


class InvoiceService:
    def __init__(self, repository: InvoiceRepository):
        self.repository = repository

    async def get_overdue_with_pending_balance(
        self,
    ) -> list[OverdueInvoiceResponse]:

        rows = await self.repository.get_overdue_with_pending_balance()

        return [
            OverdueInvoiceResponse.model_validate(row)
            for row in rows
        ]
