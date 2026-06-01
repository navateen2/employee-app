"""ORM entities."""

from models.employee import Employee, Address
from models.department import Department
from models.employee_department import EmployeeDepartment

__all__ = ["Employee", "Address", "Department", "EmployeeDepartment"]
