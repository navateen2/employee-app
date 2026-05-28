from fastapi import APIRouter, Depends,Body, HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import get_db
import services.employee_service as employee_service


router=APIRouter(prefix="/employee",tags=["Employees"])


@router.post("", status_code=status.HTTP_201_CREATED, tags=["Employees"])
async def create_employee(body: dict = Body(...), db: AsyncSession = Depends(get_db)):
    name = body.get("name")
    email = body.get("email")
    employee=await employee_service.create(db,name,email)
    
    return employee.to_api_dict()



@router.get("/", tags=["Employees"])
async def get_all_employees(db: AsyncSession = Depends(get_db)):
    
    
    return employee_service.all(db)
    return [r.to_api_dict() for r in result.all()]