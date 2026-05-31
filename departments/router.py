from fastapi import APIRouter, Depends,Body, HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import get_db
from departments import service as department_service
from departments.schemas import DepartmentCreate,DepartmentUpdate,DepartmentResponse,DepartmentIDResponse
# import services.employee_service as employee_service
from auth.schemas import TokenPayload
from auth.dependencies import get_current_user

router=APIRouter(prefix="/department",tags=["Departments"])


@router.post("", status_code=status.HTTP_201_CREATED, tags=["Departments"],response_model=DepartmentResponse)
async def create_department(body:DepartmentCreate=Body(...),db: AsyncSession = Depends(get_db)):
    department=await department_service.create(db,body)
    
    return department



@router.get("/", tags=["Departments"])
async def get_all_departments(db: AsyncSession = Depends(get_db),_current_user:TokenPayload=Depends(get_current_user))->list[dict]:
    a=await department_service.all(db)
    
    return a



@router.patch("/{department_id}", tags=["Departments"])
async def update_department(department_id: int, body: DepartmentUpdate = Body(...), db: AsyncSession = Depends(get_db)):

    name = body.name

    department= await department_service.update_department(department_id,name,db)
    

    return department

@router.get("/{department_id}", tags=["Departments"],response_model=DepartmentIDResponse)
async def get_by_id(department_id:int,db:AsyncSession= Depends(get_db))->dict:
    department=await department_service.get_by_id(department_id,db)
    return department