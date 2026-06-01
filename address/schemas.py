from pydantic import BaseModel,Field,field_validator,ConfigDict,EmailStr,model_validator

class AddessCreate(BaseModel):
    employee_id:int
    line1:str
    city:str
    country:str
    postal_code:int