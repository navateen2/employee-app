"""
Employee entity — ORM mapped class for table `employees`.
"""

from datetime import datetime
from typing import Any, Optional

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.connection import Base
from models.entity import Entity
from models.address import Address
import enum
from sqlalchemy import Enum

def _datetime_to_iso(value: datetime | None) -> str | None:
    if value is None:
        return None
    return value.isoformat()

class EmployeeRole(str,enum.Enum):
    UI="UI"
    UX="UX"
    DEVELOPER = "Developer"
    HR = "HR"



class Employee(Entity):
    __abstract__=False
    __tablename__ = "employees"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    age: Mapped[int]=mapped_column(Integer,nullable=True)
    addresses: Mapped[list["Address"]] = relationship(
        "Address",
        back_populates="employee",
    )
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    role: Mapped[EmployeeRole] = mapped_column(
        Enum(EmployeeRole, name="employeerole",values_callable=lambda enum_cls: [e.value for e in enum_cls]),
        nullable = False,
        server_default=EmployeeRole.DEVELOPER.value
    )

    def to_api_dict(self) -> dict[str, Any]:
        """JSON-friendly representation (ISO 8601 for timestamps)."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "age": self.age,
            "created_at": _datetime_to_iso(self.created_at),
            "updated_at": _datetime_to_iso(self.updated_at),
            "deleted_at": _datetime_to_iso(self.deleted_at),
        }
    


