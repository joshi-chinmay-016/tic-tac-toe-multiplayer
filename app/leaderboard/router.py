from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.leaderboard import service

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])

@router.get("/")
def read_leaderboard(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = service.get_leaderboard(db, skip=skip, limit=limit)
    return [
        {
            "id": u.id,
            "username": u.username,
            "rating": u.rating,
            "wins": u.wins,
            "losses": u.losses,
            "draws": u.draws,
            "games_played": u.games_played,
            "win_rate": round(u.wins / u.games_played * 100) if u.games_played > 0 else 0,
            "current_streak": u.current_streak
        }
        for u in users
    ]
