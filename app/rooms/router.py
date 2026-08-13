from app.api.dependencies import get_current_user
from app.models.user import User
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.rooms import service
from app.core.rate_limit import check_rate_limit

router = APIRouter(prefix="/rooms", tags=["rooms"])

@router.post("/create", dependencies=[Depends(check_rate_limit)])
async def create_private_room(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = current_user.id
    code = await service.create_room(db, user_id)
    return {"code": code, "message": "Room created"}

@router.post("/join", dependencies=[Depends(check_rate_limit)])
async def join_private_room(code: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = current_user.id
    result = await service.join_room(db, code.upper(), user_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result
