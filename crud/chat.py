from sqlalchemy.orm import Session
from models.chat import ChatMessage

def create_chat_message(db:Session,role:str,content:str):
    msg = ChatMessage(role=role,content=content)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg

def get_recent_messages(db:Session,limit:int=10):
    msgs = db.query(ChatMessage).order_by(ChatMessage.created_at.desc()).limit(limit).all()
    msgs.reverse()
    return msgs
