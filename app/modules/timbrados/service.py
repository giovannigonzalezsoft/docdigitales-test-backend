from app.modules.invoices.repository import InvoiceRepository
from app.modules.timbrados.exceptions import InvoiceNotFoundException
from app.modules.timbrados.models import Timbrado
from app.integrations.pac_gateway import PacGateway
from app.modules.timbrados.repository import TimbradoRepository
from app.modules.timbrados.schemas import (
    TimbradoCreate,
    TimbradoResponse,
)


class TimbradoService:
    def __init__(
        self,
        repository: TimbradoRepository,
        invoice_repository: InvoiceRepository,
        pac_gateway: PacGateway,
    ):
        self.repository = repository
        self.invoice_repository = invoice_repository
        self.pac_gateway = pac_gateway

    async def create(
    self,
    data: TimbradoCreate,
    ) -> tuple[TimbradoResponse, bool]:

        existing = await self.repository.get_by_external_id(
            data.external_id
        )

        if existing:
            return (
                TimbradoResponse.model_validate(existing),
                False,
            )

        invoice = await self.invoice_repository.get_by_id(
            data.invoice_id
        )

        if invoice is None:
            raise InvoiceNotFoundException(data.invoice_id)

        pac_result = await self.pac_gateway.stamp(
            invoice=invoice,
        )

        timbrado = Timbrado(
            external_id=data.external_id,
            status="timbrada" if pac_result.success else "fallida",
            uuid_fiscal=pac_result.uuid_fiscal,
            error=pac_result.error,
        )

        timbrado = await self.repository.create(timbrado)

        return (
            TimbradoResponse.model_validate(timbrado),
            True,
        )
