from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,DeclarativeBase

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@localhost:3306/agent_db"
engine = create_engine(SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()