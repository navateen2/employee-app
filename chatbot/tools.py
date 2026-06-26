from fastapi import Depends

from database.connection import get_db
from employees.repository import get_by_id

async def get_employee(employee_id:int):
    '''This is used to retrieve entire record of an employee'''
    return {
        "name":"navaneet",
        "age":20,
        "salary":700000
    }
    return await get_by_id(employee_id,Depends(get_db))
    






TOOL_FUNCTIONS={
    "get_employee":get_employee
}   



tools=tools = [
    {
        "type": "function",
        "function": {
            "name": "get_employee",
            "description": "Returns an employee's details",
            "parameters": {
                "type": "object",
                "properties": {
                    "employee_id": {
                        "type": "string",
                        "description": "Employee ID"
                    }
                },
                "required": ["employee_id"]
            }
        }
    }
]