from sqlalchemy.ext.asyncio import AsyncSession
from exceptions import *
from repositories import employee_repo
from auth.utils import verify_password,create_access_token

async def login(db:AsyncSession, email:str, password:str)->str:
    employee= await employee_repo.get_by_email(db, email)
    if employee is None:
        raise UnauthorizedException("Invalid email or password")
    if not verify_password(password, employee.password_hash):
        raise UnauthorizedException("Invalid email or password")
    return create_access_token({
        "id":employee.id,
        "email":employee.email
    })