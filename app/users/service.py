from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user import User

def get_user_profile(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user.id,
        "username": user.username,
        "rating": user.rating,
        "games_played": user.games_played,
        "wins": user.wins,
        "losses": user.losses,
        "draws": user.draws,
        "win_rate": round(user.wins / user.games_played * 100) if user.games_played > 0 else 0,
        "current_streak": user.current_streak,
        "best_streak": user.best_streak,
        "created_at": user.created_at
    }
