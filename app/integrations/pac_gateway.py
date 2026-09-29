from dataclasses import dataclass
from uuid import UUID, uuid4

from app.modules.invoices.models import Invoice


@dataclass
class PacResult:
    success: bool
    uuid_fiscal: UUID | None = None
    error: str | None = None


class PacGateway:
    def __init__(self, should_fail: bool = False):
        self.should_fail = should_fail

    async def stamp(
        self,
        invoice: Invoice,
    ) -> PacResult:
        """
        Description:
            Simulates sending an invoice to the external PAC.

        Returns:
            PacResult with the fiscal UUID or error.
        """

        if self.should_fail:
            return PacResult(
                success=False,
                error="timeout",
            )

        return PacResult(
            success=True,
            uuid_fiscal=uuid4(),
        )
