import os
import dotenv

from fastapi import APIRouter, FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, json

from litellm import acompletion

from llama_index.core import (
VectorStoreIndex,
SimpleDirectoryReader,
)

from chatbot.retriever import retriever

from . import (tools as t)

dotenv.load_dotenv()
router = APIRouter(prefix="", tags=["Employees"])

MODEL = "openai/gpt-4o-mini"



sessions = {}




class ChatRequest(BaseModel):
    session_id: str
    message: str

@router.post("/chat")
async def chat(req: ChatRequest):

    history = sessions.setdefault(req.session_id, [])

    nodes = retriever.retrieve(req.message)

    context = "\n\n".join(node.text for node in nodes)

    messages = [
        {
            "role": "system",
            "content": f"""
    You are an HR assistant.

    you have the capabliity to fetch data of employees with their id
    Answer ONLY using the company policies below and fetched data(if fetched).

    If the answer cannot be found in the policies, say so.
    POLICIES:
    {context}
    """,
    }
    ]


    messages.extend(history)

    messages.append(
        {
            "role": "user",
            "content": req.message,
        }
    )

    async def generate():

        assistant_text = ""

        stream = await acompletion(
            model=MODEL,
            messages=messages,
            stream=True,
            temperature=0.2,
            tools=t.tools,
            tool_choice="auto",
        )

        
        async for chunk in stream:

            delta = chunk.choices[0].delta.content

            if delta:
                assistant_text += delta
                yield delta

        history.append(
            {
                "role": "user",
                "content": req.message,
            }
        )

        history.append(
            {
                "role": "assistant",
                "content": assistant_text,
            }
        )

    return StreamingResponse(
        generate(),
        media_type="text/plain",
    )
    
