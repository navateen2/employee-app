from fastapi import FastAPI,Depends,HTTPException,status,Body
from typing import TypedDict
from fastapi.middleware.cors import CORSMiddleware
import logging
from middleware.logger import RequestLoggingMiddleware
from contextlib import asynccontextmanager
from database.connection import create_tables,get_db
from models.employee import Employee
from database.connection import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from routers.employee_router import router as employee_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="logs.txt"
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield

app = FastAPI(
    title="Employee CRUD API",
    description="Simple APIwith dict storage",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Process-Time"],
)

# class Employee(TypedDict):
#     id:int
#     name:str
#     # email:str
#     # department:str
#     # salary:int
#     # is_deleted:bool

E:dict[int,Employee]={}


@app.get("/")
def home():
    return "Welcome"


# @app.get("/Employees",response_model=dict[int,Employee])
# def a():
#     return E

# @app.post("/Employee/add",status_code=201)
# def create(name:str):
#     print("hii")
#     if E:
#         tid=max(E.keys())+1
#         E[tid]={"id":tid,"name":name}
#     else:
#         E[0]={"id":0,"name":name}
#     return "end"

# @app.patch("Employee/update")
# def empl_update():
#     pass
# #end point to fetch existing employees

# # @app.get("/hello",tags=["hello world"],response_model=list[str])
# # def hello():
# #     l:list[str]=[]
# #     for i in _posts.keys():
# #         l.append(_posts[i]["title"])
# #     return l

# # @app.post("/posts", tags=["Posts"], status_code=201, response_model=PostPublic)
# # def create_post(post: PostCreate):
# #     global _next_id
# #     global _posts
# #     id = _next_id
# #     _posts[_next_id] = {
# #         "id": id,
# #         "title": post.title,
# #         "body": post.body
# #     }
# #     _next_id += 1

# #     return _posts[id]

app.include_router(employee_router)




@app.patch("/employee/{employee_id}", tags=["Employees"])
async def update_employee(employee_id: int, body: dict = Body(...), db: AsyncSession = Depends(get_db)):
    stmt = select(Employee).where(Employee.id == employee_id, Employee.deleted_at.is_(None))
    result = await db.scalar(stmt)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with id {employee_id} not found")
    employee: Employee = result
    name = body.get("name")
    email = body.get("email")
    if name is not None:
        if not isinstance(name, str) or not name.strip():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="name must be a non-empty string")
        employee.name = name.strip()
    if email is not None:
        if not isinstance(email, str) or not email.strip():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email must be a non-empty string")
        employee.email = email.strip()
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Email '{email.strip()}' is already in use")
    await db.refresh(employee)
    return employee.to_api_dict()


@app.delete("/employee/{employee_id}", tags=["Employees"])
async def delete_employee(id:int, body:dict = Body(...),db:AsyncSession=Depends(get_db)):
    stmt=delete(Employee).where(Employee.id==id)
    result = await db.scalar(Employee)
    db.delete(Employee)
    db.commit()
