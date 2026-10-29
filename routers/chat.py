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
from datetime import datetime


load_dotenv()
router = APIRouter(prefix="/chat", tags=["AI导师"])

api_key=os.getenv("DEEPSEEK_API_KEY")


client = AsyncOpenAI(api_key=api_key,base_url="https://api.deepseek.com")

class ChatRequest(BaseModel):
    message: str
    user_id: str

system_prompt = """
你是一个务实、温柔、懂年轻人技术路线的赛博导师。
你知道用户是一个211大二学生，正在死磕 FastAPI 和 AI Agent，目标是找大厂实习。
当用户跟你说话时：
1. 绝对不熬空洞的鸡汤。
2. 先共情他的情绪，然后给出极其具体的、可执行的微小行动清单。
"""



def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

tools = [
    {
        "type":"function",
        "function":{
            "name":"get_current_time",
            "description":"获取真实时间",
            "parameters":{"type":"object","properties":{}}
        }
    }
]


@router.post("/")
async def chat(request: ChatRequest,db: Session=Depends(get_db)):
    try:
        crud_chat.create_chat_message(db,user_id=request.user_id, role="user",content=request.message)

        recent_msgs = crud_chat.get_recent_messages(db,user_id=request.user_id,limit=10)


        messages = [{"role":"system","content":system_prompt}]
        for msg in recent_msgs:
            messages.append({"role":msg.role,"content":msg.content})



        async def generate_response():
            full_reply = ""
            try:
                response = await client.chat.completions.create(
                    model="deepseek-chat",
                    messages=messages,
                    tools=tools,
                    stream=False
                )
                response_message = response.choices[0].message
                if response_message.tool_calls:
                    tool_call = response_message.tool_calls[0]
                    function_name = tool_call.function.name
                    if function_name == "get_current_time":
                        current_time = get_current_time()

                        messages.append(response_message.model_dump())
                        messages.append({
                            "role":"tool",
                            "tool_call_id":tool_call.id,
                            "name":function_name,
                            "content":current_time
                        })
                        final_response = await client.chat.completions.create(
                            model="deepseek-chat",
                            messages=messages,
                            stream = True
                        )
                        async for chunk in final_response:
                            content = chunk.choices[0].delta.content
                            if content:
                                full_reply += content
                                yield content

                else:
                    full_reply = response_message.content
                    yield full_reply


                crud_chat.create_chat_message(db,user_id=request.user_id,role="assistant",content=full_reply)
            except Exception as e:
                yield f"\n[发生错误: {str(e)}]"
        return StreamingResponse(generate_response(),media_type="text/event-stream")



    except Exception as e:
        return {"status":"error","message":str(e)}