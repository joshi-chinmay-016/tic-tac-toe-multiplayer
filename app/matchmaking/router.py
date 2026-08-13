from app.api.dependencies import get_current_user
from app.models.user import User
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.matchmaking import service
from app.core.rate_limit import check_rate_limit

router = APIRouter(prefix="/matchmaking", tags=["matchmaking"])

@router.post("/join", dependencies=[Depends(check_rate_limit)])
async def join_matchmaking(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = current_user.id
    result = await service.process_matchmaking(db, user_id)
    if result:
        return {"message": "Match created", **result}
    return {"message": "Waiting for opponent"}
