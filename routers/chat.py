import os
from dotenv import load_dotenv
from fastapi import APIRouter,Depends
from pydantic import BaseModel
from openai import AsyncOpenAI
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from models.chat import ChatMessage
from crud import chat as crud_chat
from db.session import get_db


load_dotenv()
router = APIRouter(prefix="/chat", tags=["AI导师"])

api_key=os.getenv("DEEPSEEK_API_KEY")


client = AsyncOpenAI(api_key=api_key,base_url="https://api.deepseek.com")

class ChatRequest(BaseModel):
    message: str

system_prompt = """
你是一个务实、温柔、懂年轻人技术路线的赛博导师。
你知道用户是一个211大二学生，正在死磕 FastAPI 和 AI Agent，目标是找大厂实习。
当用户跟你说话时：
1. 绝对不熬空洞的鸡汤。
2. 先共情他的情绪，然后给出极其具体的、可执行的微小行动清单。
"""


@router.post("/")
async def chat(request: ChatRequest,db: Session=Depends(get_db)):
    try:
        crud_chat.create_chat_message(db,role="user",content=request.message)

        recent_msgs = crud_chat.get_recent_messages(db,limit=10)


        messages = [{"role":"system","content":system_prompt}]
        for msg in recent_msgs:
            messages.append({"role":msg.role,"content":msg.content})



        async def generate_response():
            full_reply = ""
            try:
                response = await client.chat.completions.create(
                    model="deepseek-chat",
                    messages=messages,
                    stream=True
                )
                async for chunk in response:
                    content = chunk.choices[0].delta.content
                    if content:
                        full_reply += content
                        yield content

                crud_chat.create_chat_message(db,role="assistant",content=full_reply)
            except Exception as e:
                yield f"\n[发生错误: {str(e)}]"
        return StreamingResponse(generate_response(),media_type="text/event-stream")



    except Exception as e:
        return {"status":"error","message":str(e)}