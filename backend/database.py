import os
from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
engine = create_engine(f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}/{os.getenv('MYSQL_DATABASE')}")
Base = declarative_base()

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(String(255), primary_key=True)
    user_id = Column(String(255))
    message = Column(String(1000))
    category = Column(String(100))
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
class User(Base):
    __tablename__ = "users"
    
    uid = Column(String(255), primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(255))
    age_group = Column(String(50))
    gender = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

def save_user(uid: str, email: str, name: str, age_group: str = None, gender: str = None):
    session = Session()
    try:
        user = User(
            uid=uid,
            email=email,
            name=name,
            age_group=age_group,
            gender=gender
        )
        session.add(user)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def get_user_profile(uid: str) -> dict:
    session = Session()
    try:
        user = session.query(User).filter(User.uid == uid).first()
        if user:
            return {
                "uid": user.uid,
                "email": user.email,
                "name": user.name,
                "age_group": user.age_group,
                "gender": user.gender
            }
        return None
    finally:
        session.close()