from app.modules.clients.repository import ClientRepository
from app.modules.clients.schemas import ClientBillingSummaryResponse


class ClientService:
    def __init__(self, repository: ClientRepository):
        self.repository = repository

    async def get_billing_summary(
        self,
    ) -> list[ClientBillingSummaryResponse]:

        rows = await self.repository.get_billing_summary()

        return [
            ClientBillingSummaryResponse.model_validate(row)
            for row in rows
        ]
