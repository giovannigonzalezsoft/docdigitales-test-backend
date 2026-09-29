from uuid import UUID

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class Timbrado(Base):
    __tablename__ = "timbrados"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )
    external_id: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )
    uuid_fiscal: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=True,
    )
    error: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
