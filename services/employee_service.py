import repositories.employee_repo as employee_repo
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from models.employee import Employee

async def create(db:AsyncSession,name:str,email:str)->Employee:
    if not isinstance(name, str) or not name.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="name must be a non-empty string")
    if not isinstance(email, str) or not email.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email must be a non-empty string")
    employee = await employee_repo.create(db,name.strip(),email.strip())
    return employee

async def all(db:AsyncSession)->list[dict]:
    return await employee_repo.all(db)
    
async def update_employee(employee_id: int,name:str,email:str, db: AsyncSession)->Employee:
    if name is not None:
        if not isinstance(name, str) or not name.strip():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="name must be a non-empty string")
        
    if email is not None:
        if not isinstance(email, str) or not email.strip():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email must be a non-empty string")
        
    return employee_repo.update_employee(employee_id,name.strip(),email.strip(),db)

async def get_by_id(employee_id:int,db:AsyncSession)->Employee:
    return await employee_repo.get_by_id(employee_id,db)