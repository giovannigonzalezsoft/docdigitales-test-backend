from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator
from decimal import Decimal, InvalidOperation
from typing import Any


class TimbradoCreate(BaseModel):
    external_id: str = Field(min_length=1, max_length=100)
    invoice_id: int = Field(gt=0)
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)

    @field_validator("external_id", mode="before")
    @classmethod
    def validate_external_id(cls, value: Any) -> str:
        if not isinstance(value, str):
            raise ValueError("Debe ser una cadena de texto")

        value = value.strip()

        if not value:
            raise ValueError("Es obligatorio")

        if len(value) > 100:
            raise ValueError("No puede exceder los 100 caracteres")

        return value

    @field_validator("invoice_id", mode="before")
    @classmethod
    def validate_invoice_id(cls, value: Any) -> int:
        if isinstance(value, bool):
            raise ValueError("Debe ser un número entero")

        try:
            value = int(value)
        except (TypeError, ValueError):
            raise ValueError("Debe ser un número entero")

        if value <= 0:
            raise ValueError("Debe ser mayor que 0")

        return value

    @field_validator("amount", mode="before")
    @classmethod
    def validate_amount(cls, value: Any) -> Decimal:
        try:
            value = Decimal(str(value))
        except (InvalidOperation, TypeError, ValueError):
            raise ValueError("Debe ser un valor numérico")

        if value <= 0:
            raise ValueError("Debe ser mayor que 0")

        return value


class TimbradoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    status: str
    external_id: str
    uuid_fiscal: UUID | None = None
    error: str | None = None
