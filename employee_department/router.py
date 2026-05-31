# - Attach department to an employee -> /{employee_id}/departments/{department_id}
# - Detach employee from department -> /{employee_id}/departments/{department_id}
# - Delete address of an employee -> /{employee_id}/addresses/{address_id}

from fastapi import APIRouter, Depends,Body, HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import get_db
from employees import service as employee_service
from employees.schemas import EmployeeCreate,EmployeeUpdate,EmployeeResponse,EmployeeIDResponse
# import services.employee_service as employee_service
from auth.schemas import TokenPayload
from auth.dependencies import get_current_user
from models.employee_department import EmployeeDepartment
from exceptions import *
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from datetime import datetime,timezone
router=APIRouter(prefix="",tags=["Employees"])


@router.post("/{employee_id}/departments/{department_id}", status_code=status.HTTP_201_CREATED, tags=["Employees-Department"])
async def createEmployeeDepartment(employee_id:int,department_id:int,db: AsyncSession = Depends(get_db),):
    db_ed = EmployeeDepartment(employee_id=employee_id,department_id=department_id)
    db.add(db_ed)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        # raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Email '{email.strip()}' is already in use")
        raise ConflictException
    await db.refresh(db_ed)
    return db_ed


@router.delete("/{employee_id}/departments/{department_id}", status_code=status.HTTP_201_CREATED, tags=["Employees-Department"])
async def deleteEmployeeDepartment(employee_id:int,department_id:int,db: AsyncSession = Depends(get_db),):

    stmt = select(EmployeeDepartment).where(
        EmployeeDepartment.employee_id == employee_id,
        EmployeeDepartment.department_id == department_id,
        EmployeeDepartment.deleted_at.is_(None)
    )

    association = await db.scalar(stmt)

    if association is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee-Department association not found"
        )

    association.deleted_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(association)
    return "success"