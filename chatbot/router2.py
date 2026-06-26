import os
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from langchain.messages import AIMessage
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from pydantic import BaseModel
from .tools2 import search_hr_policy,get_employee

router = APIRouter(prefix="", tags=["Employees"])

from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
    streaming=True,
)


agent = create_agent(
    llm,
    tools=[
        search_hr_policy,
        get_employee,
    ],
)



session={}

class ChatRequest(BaseModel):
    session_id: str
    message: str

@router.post("/chat")
async def chat(req: ChatRequest):

    async def generate():
        async for message, metadata in agent.astream(
            {"messages": [
                    (
                        "system",
                        """
                        You are an HR assistant.

                        Answer HR policy questions using the HR policy tool.

                        Use the employee tool whenever the user asks about an employee's
                        personal information, salary, etc.

                        Never invent employee information.
                        """
                    ),
                    ("user", req.message),
                ]},
            stream_mode="messages",
        ):
            if (
                isinstance(message, AIMessage)
                and not message.tool_calls
                and message.content
            ):
                # logging.info(f"Agent message: {message.content}")
                yield message.content
        

    return StreamingResponse(
        generate(),
        media_type="text/plain",
    )