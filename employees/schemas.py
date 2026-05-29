from pydantic import BaseModel,Field,field_validator,ConfigDict,EmailStr,model_validator
from datetime import datetime
class AddressCreate(BaseModel):
    country:str
    city:str
    postal_code:str
    country:str

    @field_validator("postal_code")
    @classmethod
    def validate_postal_code(cls, v: str) -> str:
        if not v.isdigit():
            raise ValueError("Postal code must contain only digits (0-9)")
        return v
    
    @model_validator(mode="after")
    def postal_code_length_for_country(self):

        country = self.country.strip().upper()

        n = len(self.postal_code)

        if country in ("US", "USA") and n != 5:

            raise ValueError("US ZIP codes must be exactly 5 digits")

        elif country == "IN" and n != 6:

            raise ValueError("Indian PIN codes must be exactly 6 digits")

        return self
    



class EmployeeCreate(BaseModel):
    model_config=ConfigDict(str_max_length=10,extra='forbid')
    name:str = Field(min_length=1,max_length=50)
    email:EmailStr
    age:int | None = Field(ge=18,le=150)
    address: AddressCreate | None = None


class EmployeeUpdate:
    name:str


class EmployeeResponse(BaseModel):
    model_config=ConfigDict(
        from_attributes=True

    )
    id:int
    name:str
    email:str
    age:int|None

class EmployeeIDResponse(BaseModel):
    model_config=ConfigDict(
        from_attributes=True

    )
    created_at:datetime
    updated_at:datetime
    deleted_at:datetime

    