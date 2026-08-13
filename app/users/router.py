from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.users import service

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{username}")
def read_user_profile(username: str, db: Session = Depends(get_db)):
    return service.get_user_profile(db, username)
