from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from models.entity import Entity


class EmployeeDepartment(Entity):
    __tablename__ = "employee_departments"

    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"), nullable=False)

    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.id"), nullable=False
    )
