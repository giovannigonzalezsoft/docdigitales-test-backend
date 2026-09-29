from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_serializer


class OverdueInvoiceResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "invoice_id": 1,
                "folio": "FAC-001",
                "client_id": 1,
                "pending_balance": 800,
            }
        }
    )

    invoice_id: int
    folio: str
    client_id: int
    pending_balance: Decimal = Field(decimal_places=2)

    @field_serializer("pending_balance")
    def serialize_decimal(self, value: Decimal) -> float:
        return float(value)
