from fastapi import FastAPI,Depends,HTTPException,status,Body
from typing import TypedDict
import logging
import middleware as m
from contextlib import asynccontextmanager
from database.connection import create_tables,get_db
from models.employee import Employee
from database.connection import AsyncSession

from routers.employee_router import router as employee_router
from config import APP_ENV



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
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
m.configure_middleware(app)


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

@app.get("/health")
def health():
    return {"status":"healthy","message":"running","Environment":APP_ENV}
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






# @app.delete("/employee/{employee_id}", tags=["Employees"])
# async def delete_employee(id:int, body:dict = Body(...),db:AsyncSession=Depends(get_db)):
#     stmt=delete(Employee).where(Employee.id==id)
#     result = await db.scalar(Employee)
#     db.delete(Employee)
#     db.commit()
