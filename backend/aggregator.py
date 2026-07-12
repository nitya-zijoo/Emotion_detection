from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from database import Message
import os

engine = create_engine(f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}/cd{os.getenv('MYSQL_DATABASE')}")
Session = sessionmaker(bind=engine)

def get_category_counts(user_id: str) -> dict:
    session = Session()
    cutoff = datetime.utcnow() - timedelta(days=14)
    
    results = session.query(
        Message.category,
        func.count(Message.category).label("count")
    ).filter(
        Message.user_id == user_id,
        Message.timestamp >= cutoff
    ).group_by(Message.category).all()
    
    session.close()
    return {row.category: row.count for row in results}