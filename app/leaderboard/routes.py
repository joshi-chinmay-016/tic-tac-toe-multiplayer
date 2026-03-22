from fastapi import APIRouter
from app.database import SessionLocal
from app.models.user import User

router = APIRouter(prefix="/leaderboard")

@router.get("/")
def leaderboard():
    db = SessionLocal()
    users = db.query(User).all()

    result = []
    for u in users:
        result.append({
            "id": u.id,
            "username": u.username,
            "wins": u.wins,
            "losses": u.losses
        })

    db.close()
    return result
