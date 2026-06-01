from fastapi import APIRouter, Depends,Body, HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import get_db
from employees import service as employee_service
from employees.schemas import EmployeeCreate,EmployeeUpdate,EmployeeResponse,EmployeeIDResponse
# import services.employee_service as employee_service
from auth.schemas import TokenPayload
from auth.dependencies import get_current_user,require_role
from models.employee import EmployeeRole
router=APIRouter(prefix="/employee",tags=["Employees"])


@router.post("", status_code=status.HTTP_201_CREATED, tags=["Employees"],response_model=EmployeeResponse, dependencies=[Depends(require_role(EmployeeRole.HR))])
async def create_employee(body:EmployeeCreate=Body(...),db: AsyncSession = Depends(get_db), _current_user:TokenPayload=Depends(get_current_user)):
    employee=await employee_service.create(db,body)
    
    return employee



@router.get("/", tags=["Employees"], dependencies=[Depends(require_role(EmployeeRole.HR))])
async def get_all_employees(db: AsyncSession = Depends(get_db), _current_user:TokenPayload=Depends(get_current_user))->list[dict]:
    a=await employee_service.all(db)
    
    return a



@router.patch("/{employee_id}", tags=["Employees"], dependencies=[Depends(require_role(EmployeeRole.HR))])
async def update_employee(employee_id: int, body: dict = Body(...), db: AsyncSession = Depends(get_db), _current_user:TokenPayload=Depends(get_current_user)):
    
    
    name = body.name
    email = body.email

    employee= await employee_service.update_employee(employee_id,name,email,db)
    

    return employee

@router.get("/{employee_id}", tags=["Employees"],response_model=EmployeeIDResponse, dependencies=[Depends(require_role(EmployeeRole.HR))])
async def get_by_id(employee_id:int,db:AsyncSession= Depends(get_db), _current_user:TokenPayload=Depends(get_current_user))->dict:
    employee=await employee_service.get_by_id(employee_id,db)
    return employee


@router.delete("/{employee_id}", status_code=status.HTTP_201_CREATED, tags=["Employees"], dependencies=[Depends(require_role(EmployeeRole.HR))])
async def deleteEmployee(employee_id:int,db: AsyncSession = Depends(get_db), _current_user:TokenPayload=Depends(get_current_user)):
    return await employee_service.deleteEmployee(employee_id,db)
