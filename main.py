from fastapi import FastAPI
import logging
import middleware as m
from contextlib import asynccontextmanager
from employees.router import router as employee_router
from departments.router import router as department_router
from employee_department.router import router as ed_router

# from routers.employee_router import router as employee_router
from config import settings
from exceptions.handlers import register_exception_handlers
from auth.router import router as auth_router
from database.connection import create_tables
from address.router import router as address_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="info.log",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await create_tables()
    yield


app = FastAPI(
    title="Employee CRUD API",
    description="Simple APIwith dict storage",
    version="1.0.0",
    lifespan=lifespan,
)


m.configure_middleware(app)
register_exception_handlers(app)


@app.get("/")
def home():
    return "Welcome"


@app.get("/health")
def health():
    return {"status": "healthy", "message": "running", "Environment": settings.app_env}


app.include_router(employee_router)
app.include_router(department_router)
app.include_router(auth_router)
app.include_router(ed_router)
app.include_router(address_router)
