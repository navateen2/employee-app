from pydantic import BaseModel


class AddessCreate(BaseModel):
    employee_id: int
    line1: str
    city: str
    country: str
    postal_code: int
