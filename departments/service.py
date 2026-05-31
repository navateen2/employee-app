from departments import repository
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from models.department import Department
from auth.utils import hash_password
async def create(db:AsyncSession,body)->Department:
    hashed=hash_password(body.password)
    department = await repository.create(db,body.name.strip(),body.email.strip(),password_hash=hashed,age=body.age)
    return department

async def all(db:AsyncSession)->list[dict]:
    return await repository.all(db)
    
async def update_department(department_id: int,name:str,email:str, db: AsyncSession)->Department:
    return await repository.update_employee(department_id,name.strip(),email.strip(),db)

async def get_by_id(department_id:int,db:AsyncSession)->Department:
    return await repository.get_by_id(department_id,db)


