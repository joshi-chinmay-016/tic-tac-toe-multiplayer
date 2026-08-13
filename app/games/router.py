from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.models.game import Game
from app.models.game_event import GameEvent
from app.games.service import GameService

router = APIRouter(prefix="/games", tags=["games"])

@router.get("/history/{username}")
async def get_match_history(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    games = db.query(Game).filter(
        (Game.player_x_id == user.id) | (Game.player_o_id == user.id)
    ).order_by(Game.created_at.desc()).limit(50).all()

    result = []
    for g in games:
        opponent = "AI" if g.game_type == "vs_ai" else "Opponent"
        if g.game_type == "multiplayer" or g.game_type == "private":
            opp_id = g.player_o_id if g.player_x_id == user.id else g.player_x_id
            if opp_id:
                opp_user = db.query(User).filter(User.id == opp_id).first()
                if opp_user:
                    opponent = opp_user.username

        result.append({
            "id": g.id,
            "type": g.game_type,
            "opponent": opponent,
            "status": g.status,
            "winner": g.winner,
            "date": g.created_at.isoformat() if g.created_at else None
        })

    return result

@router.get("/{game_id}/replay")
async def get_game_replay(game_id: int, db: Session = Depends(get_db)):
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    events = db.query(GameEvent).filter(GameEvent.game_id == game_id).order_by(GameEvent.move_number.asc()).all()

    moves = []
    for e in events:
        moves.append({
            "move_number": e.move_number,
            "symbol": e.symbol,
            "position": e.position
        })

    return {
        "game_id": game.id,
        "type": game.game_type,
        "winner": game.winner,
        "moves": moves
    }
