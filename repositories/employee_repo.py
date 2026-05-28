from fastapi import HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from models.employee import Employee


async def create(db:AsyncSession,name:str, email:str) -> Employee:
    db_employee = Employee(name=name.strip(), email=email.strip())
    db.add(db_employee)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Email '{email.strip()}' is already in use")
    await db.refresh(db_employee)
    return db_employee


async def all(db:AsyncSession)->list[Employee]:
    stmt = select(Employee).where(Employee.deleted_at.is_(None))
    await db.scalars(stmt)
    
