"""
Address entity — ORM mapped class for table `Address`.
"""

from datetime import datetime
from typing import Any, Optional

from sqlalchemy import DateTime, Integer, String, func,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database.connection import Base
from models.entity import Entity


def _datetime_to_iso(value: datetime | None) -> str | None:
    if value is None:
        return None
    return value.isoformat()


class Address(Entity):
    __abstract__=False
    __tablename__ = "addresses"
    employee_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("employees.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    line1: Mapped[str] = mapped_column(String(100), nullable=False)
    city: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    postal_code: Mapped[int]=mapped_column(Integer,nullable=True)
    country: Mapped[str] = mapped_column(String(100), nullable=False)

    # def to_api_dict(self) -> dict[str, Any]:
    #     """JSON-friendly representation (ISO 8601 for timestamps)."""
    #     return {
    #         "id": self.id,
    #         "name": self.name,
    #         "email": self.email,
    #         "age": self.age,
    #         "created_at": _datetime_to_iso(self.created_at),
    #         "updated_at": _datetime_to_iso(self.updated_at),
    #         "deleted_at": _datetime_to_iso(self.deleted_at),
    #     }