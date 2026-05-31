# - Delete address of an employee -> /{employee_id}/addresses/{address_id}

from fastapi import APIRouter, Depends,Body, HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import get_db
from employees import service as employee_service
from employees.schemas import EmployeeCreate,EmployeeUpdate,EmployeeResponse,EmployeeIDResponse
# import services.employee_service as employee_service
from auth.schemas import TokenPayload
from auth.dependencies import get_current_user
from models.address import Address
from exceptions import *
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from datetime import datetime,timezone
router=APIRouter(prefix="",tags=["Employees"])


@router.delete("/{employee_id}/addresses/{address_id}", status_code=status.HTTP_201_CREATED, tags=["Addresses"])
async def deleteEmployeeAddress(employee_id:int,address_id:int,db: AsyncSession = Depends(get_db),):

    stmt = select(Address).where(
        Address.employee_id == employee_id,
        Address.id == address_id,
        Address.deleted_at.is_(None)
    )

    a = await db.scalar(stmt)

    if a is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee-Address association not found"
        )

    a.deleted_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(a)
    return "success"