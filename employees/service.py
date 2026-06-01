import repositories.employee_repo as employee_repo
from sqlalchemy.ext.asyncio import AsyncSession
from models.employee import Employee
from auth.utils import hash_password


async def create(db: AsyncSession, body) -> Employee:
    hashed = hash_password(body.password)
    employee = await employee_repo.create(
        db, body.name.strip(), body.email.strip(), password_hash=hashed, age=body.age
    )
    return employee


async def all(db: AsyncSession) -> list[dict]:
    return await employee_repo.all(db)


async def update_employee(
    employee_id: int, name: str, email: str, db: AsyncSession
) -> Employee:
    return await employee_repo.update_employee(
        employee_id, name.strip(), email.strip(), db
    )


async def get_by_id(employee_id: int, db: AsyncSession) -> Employee:
    return await employee_repo.get_by_id(employee_id, db)


async def deleteEmployee(employee_id: int, db: AsyncSession):
    return await employee_repo.deleteEmployee(employee_id, db)
