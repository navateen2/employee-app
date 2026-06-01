from fastapi import APIRouter, Depends, Body, status
from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import get_db
from departments import service as department_service
from departments.schemas import (
    DepartmentCreate,
    DepartmentUpdate,
    DepartmentResponse,
    DepartmentIDResponse,
)
from models.employee import EmployeeRole
# import services.employee_service as employee_service
from auth.schemas import TokenPayload
from auth.dependencies import get_current_user,require_role

router = APIRouter(prefix="/department", tags=["Departments"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    tags=["Departments"],
    response_model=DepartmentResponse,
    dependencies=[Depends(require_role(EmployeeRole.HR))]
    
)
async def create_department(
    body: DepartmentCreate = Body(...),
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    department = await department_service.create(db, body)

    return department


#
@router.get("/", tags=["Departments"])
async def get_all_departments(
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
) -> list[dict]:
    a = await department_service.all(db)

    return a


@router.patch("/{department_id}", tags=["Departments"],
    dependencies=[Depends(require_role(EmployeeRole.HR))])
async def update_department(
    department_id: int,
    body: DepartmentUpdate = Body(...),
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):

    name = body.name

    department = await department_service.update_department(department_id, name, db)

    return department


@router.get(
    "/{department_id}", tags=["Departments"], response_model=DepartmentIDResponse
)
async def get_by_id(
    department_id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
) -> dict:
    department = await department_service.get_by_id(department_id, db)
    return department

@router.delete(
    "/{department_id}", tags=["Departments"],
    dependencies=[Depends(require_role(EmployeeRole.HR))]
)
async def delete(
    department_id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
) -> dict:
    department = await department_service.delete(department_id, db)
    return department
