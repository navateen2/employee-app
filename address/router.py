# - Delete address of an employee -> /{employee_id}/addresses/{address_id}

from fastapi import APIRouter, Depends, Body, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import get_db

# import services.employee_service as employee_service
from models.address import Address
from exceptions import *
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timezone
from address.schemas import *
from auth.schemas import TokenPayload
from auth.dependencies import get_current_user,require_role
from models.employee import EmployeeRole
router = APIRouter(prefix="", tags=["Employees"])


@router.delete(
    "/{employee_id}/addresses/{address_id}",
    status_code=status.HTTP_201_CREATED,
    tags=["Addresses"],
    dependencies=[Depends(require_role(EmployeeRole.HR))]

)
async def deleteEmployeeAddress(
    employee_id: int,
    address_id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user)
):

    stmt = select(Address).where(
        Address.employee_id == employee_id,
        Address.id == address_id,
        Address.deleted_at.is_(None),
    )

    a = await db.scalar(stmt)

    if a is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee-Address association not found",
        )

    a.deleted_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(a)
    return "success"


@router.post(
    "/{employee_id}/addresses/", status_code=status.HTTP_201_CREATED, tags=["Addresses"],dependencies=[Depends(require_role(EmployeeRole.HR))]

)
async def createEmployeeAddress(
    employee_id: int,
    body: AddessCreate = Body(...),
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user)
):

    addr = Address(
        employee_id=body.employee_id,
        line1=body.line1,
        city=body.city,
        postal_code=body.postal_code,
        country=body.country,
    )

    db.add(addr)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        # raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Email '{email.strip()}' is already in use")
        raise ConflictException
    await db.refresh(addr)
    return addr

    if a is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee-Address association not found",
        )

    a.deleted_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(a)
    return "success"
