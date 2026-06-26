from chatbot.retriever import retriever
from langchain.tools import tool

@tool
async def get_employee(employee_id:int):
    '''This is used to retrieve entire record of an employee'''
    return {
        "name":"navaneet",
        "age":20,
        "salary":700000
    }
    return await get_by_id(employee_id,Depends(get_db))

@tool
def search_hr_policy(question: str) -> str:
    """Search HR policies."""

    docs = retriever.retrieve(question)

    return "\n\n".join(
        doc.get_content()
        for doc in docs
    )