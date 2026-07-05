import os
from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
engine = create_engine("mysql+pymysql://root:nitya@localhost/emotions_db")
Base = declarative_base()

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(String, primary_key=True)
    user_id = Column(String)
    message = Column(String)
    category = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def save_message(user_id: str, message: str, category: str):
    session = Session()
    record = Message(
        id=str(datetime.utcnow().timestamp()),
        user_id=user_id,
        message=message,
        category=category
    )
    session.add(record)
    session.commit()
    session.close()