from sqlalchemy.orm import Session
from app.models.user import User

def get_leaderboard(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).order_by(User.rating.desc(), User.wins.desc()).offset(skip).limit(limit).all()
