from sqlalchemy.orm import Session
from models.chat import ChatMessage

def create_chat_message(db:Session, user_id: str,role:str,content:str):
    msg = ChatMessage(user_id=user_id,role=role,content=content)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg

def get_recent_messages(db:Session,user_id:str,limit:int=10):
    msgs = db.query(ChatMessage).filter(ChatMessage.user_id==user_id).order_by(ChatMessage.created_at.desc()).limit(limit).all()
    msgs.reverse()
    return msgs
