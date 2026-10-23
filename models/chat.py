from sqlalchemy import Column,Integer,String,DateTime
from datetime import datetime
from db.session import Base

class ChatMessage(Base):
    __tablename__ = 'chat_messages'
    id = Column(Integer,primary_key=True,index=True)
    role = Column(String(20),nullable=False)
    content = Column(String(2000),nullable=False)
    created_at = Column(DateTime,default=datetime.now())