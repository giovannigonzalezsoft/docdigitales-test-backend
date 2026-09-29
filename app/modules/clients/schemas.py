from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_serializer


class ClientBillingSummaryResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "client_id": 1,
                "client_name": "Empresa SA de CV",
                "total_invoiced": 1000,
                "total_paid": 500,
            }
        }
    )

    client_id: int
    client_name: str
    total_invoiced: Decimal = Field(decimal_places=2)
    total_paid: Decimal = Field(decimal_places=2)

    @field_serializer("total_invoiced", "total_paid")
    def serialize_decimal(self, value: Decimal) -> float:
        return float(value)
