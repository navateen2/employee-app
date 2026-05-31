from fastapi import HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from models.employee import Employee
from sqlalchemy import select,update
from exceptions import *

async def create(db:AsyncSession,name:str, email:str, password_hash:str,age:int) -> Employee:
    db_employee = Employee(name=name.strip(), email=email.strip(),age=age,password_hash=password_hash)
    db.add(db_employee)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        # raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Email '{email.strip()}' is already in use")
        raise ConflictException
    await db.refresh(db_employee)
    return db_employee


async def all(db:AsyncSession)->list[dict]:
    stmt = select(Employee).where(Employee.deleted_at.is_(None))
    result= await db.scalars(stmt)
    return [r.to_api_dict() for r in result.all()]

async def update_employee(employee_id: int, name:str,email:str,db: AsyncSession )->Employee:
    stmt = update(Employee).where(Employee.id == employee_id, Employee.deleted_at.is_(None)).values(name=name,email=email)
    result = await db.execute(stmt)
    if result is None:
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with id {employee_id} not found")
        raise NotFoundException
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        # raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Email '{email.strip()}' is already in use")
        raise ConflictException
    return await get_by_id(employee_id,db)

async def get_by_id(employee_id:int,db:AsyncSession)->Employee:
    stmt=select(Employee).where(Employee.id==employee_id)
    result=await db.scalar(stmt)
    if result is None:
        raise NotFoundException
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with id {employee_id} not found")

    return result


async def get_by_email(db:AsyncSession,email:str)->Employee | None:
    stmt=select(Employee).where(
        Employee.email == email,
        Employee.deleted_at.is_(None),
    )
    return await db.scalar(stmt)


