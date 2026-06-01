from departments import repository
from sqlalchemy.ext.asyncio import AsyncSession
from models.department import Department


async def create(db: AsyncSession, body) -> Department:
    # hashed=hash_password(body.password)
    department = await repository.create(db, body.name.strip())
    return department


async def all(db: AsyncSession):
    return await repository.all(db)


async def update_department(
    department_id: int, name: str, db: AsyncSession
) -> Department:
    return await repository.update_department(department_id, name.strip(), db)


async def delete(
    department_id: int, db: AsyncSession
):
    return await repository.delete(department_id, db)


async def get_by_id(department_id: int, db: AsyncSession) -> Department:
    return await repository.get_by_id(department_id, db)
