from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from database import Message

engine = create_engine("mysql+pymysql://username:password@localhost/emotions_db")
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