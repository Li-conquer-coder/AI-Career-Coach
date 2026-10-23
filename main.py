from fastapi import FastAPI
from routers import chat
from db.session import engine, Base
from models import chat as chat_model


Base.metadata.create_all(bind=engine)

app = FastAPI(title = "AI赛博导师")

app.include_router(chat.router)

@app.get("/")
async def read_root():
    return {"message": "AI助手已启动"}