from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.match import Match

router = APIRouter(prefix="/matchmaking")

# In-memory queue and pending match results
queue = []
pending = {}   # user_id -> {"match_id": int, "player_x": int, "player_o": int}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/join")
def join_matchmaking(user_id: int, db: Session = Depends(get_db)):

    # If this user already has a match waiting for them, return it
    if user_id in pending:
        result = pending.pop(user_id)
        return {"message": "Match created", **result}

    # Add to queue if not already in it
    if user_id not in queue:
        queue.append(user_id)

    # If two players are waiting, create a match
    if len(queue) >= 2:
        player_x = queue.pop(0)
        player_o = queue.pop(0)

        new_match = Match(
            player_x=player_x,
            player_o=player_o,
            status="playing"
        )

        db.add(new_match)
        db.commit()
        db.refresh(new_match)

        match_info = {
            "match_id": new_match.id,
            "player_x": player_x,
            "player_o": player_o
        }

        # Store result for BOTH players; return immediately for the calling player
        if player_x == user_id:
            pending[player_o] = match_info
        else:
            pending[player_x] = match_info

        return {"message": "Match created", **match_info}

    return {"message": "Waiting for opponent"}

