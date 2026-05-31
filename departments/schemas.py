from pydantic import BaseModel,Field,field_validator,ConfigDict,EmailStr,model_validator
from datetime import datetime



class Department(BaseModel):
    model_config=ConfigDict(extra='forbid')
    name:str = Field(min_length=1,max_length=50)


class DepartmentUpdate:
    name:str


class DepartmentResponse(BaseModel):
    model_config=ConfigDict(
        from_attributes=True

    )
    id:int
    name:str


class DepartmentIDResponse(BaseModel):
    model_config=ConfigDict(
        from_attributes=True

    )
    created_at:datetime
    updated_at:datetime
    deleted_at:datetime

    