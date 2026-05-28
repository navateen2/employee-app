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
async def get_all_employees(db: AsyncSession = Depends(get_db))->list[dict]:
    a=await employee_service.all(db)
    
    return a



@router.patch("/{employee_id}", tags=["Employees"])
async def update_employee(employee_id: int, body: dict = Body(...), db: AsyncSession = Depends(get_db)):
    
    
    name = body.get("name")
    email = body.get("email")

    employee= await employee_service.update_employee(employee_id,name,email,db)
    

    return employee.to_api_dict()

@router.get("/{employee_id}", tags=["Employees"])
async def get_by_id(employee_id:int,db:AsyncSession= Depends(get_db))->dict:
    employee=await employee_service.get_by_id(employee_id,db)
    return employee.to_api_dict()