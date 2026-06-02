import employees.repository as repository
from sqlalchemy.ext.asyncio import AsyncSession
from models.employee import Employee
from auth.utils import hash_password


async def create(db: AsyncSession, body) -> Employee:
    hashed = hash_password(body.password)
    employee = await repository.create(
        db, body.name.strip(), body.email.strip(), password_hash=hashed, age=body.age
    )
    return employee


async def all(db: AsyncSession) -> list[dict]:
    return await repository.all(db)


async def update_employee(
    employee_id: int, body, db: AsyncSession
) -> Employee:
    return await repository.update_employee(
        employee_id, body, db
    )


async def get_by_id(employee_id: int, db: AsyncSession) -> dict:
    return await repository.get_by_id(employee_id, db)


async def deleteEmployee(employee_id: int, db: AsyncSession):
    return await repository.deleteEmployee(employee_id, db)
