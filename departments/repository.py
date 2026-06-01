from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from models.department import Department
from sqlalchemy import select, update
from exceptions import NotFoundException, ConflictException


async def create(db: AsyncSession, name: str) -> Department:
    db_department = Department(name=name.strip())
    db.add(db_department)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        # raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Email '{email.strip()}' is already in use")
        raise ConflictException
    await db.refresh(db_department)
    return db_department


async def all(db: AsyncSession) -> list[dict]:
    stmt = select(Department).where(Department.deleted_at.is_(None))
    result = await db.scalars(stmt)
    return [r.to_api_dict() for r in result.all()]


async def update_department(
    department_id: int, name: str, db: AsyncSession
) -> Department:
    stmt = (
        update(Department)
        .where(Department.id == department_id, Department.deleted_at.is_(None))
        .values(name=name)
    )
    result = await db.execute(stmt)
    if result is None:
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Department with id {department_id} not found")
        raise NotFoundException
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        # raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Email '{email.strip()}' is already in use")
        raise ConflictException
    return await get_by_id(department_id, db)


async def get_by_id(department_id: int, db: AsyncSession) -> Department:
    stmt = select(Department).where(Department.id == department_id)
    result = await db.scalar(stmt)
    if result is None:
        raise NotFoundException
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Department with id {department_id} not found")

    return result
