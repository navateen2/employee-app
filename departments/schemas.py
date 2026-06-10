from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class Department(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str = Field(min_length=1, max_length=50)


class DepartmentCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str = Field(min_length=1, max_length=50)


class DepartmentUpdate(BaseModel):
    name: str


class DepartmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str


class DepartmentIDResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime|None
