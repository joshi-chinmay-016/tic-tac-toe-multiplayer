from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.auth.schemas import UserCreate, UserLogin, Token
from app.auth import service
from app.core.rate_limit import check_rate_limit

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", status_code=201, dependencies=[Depends(check_rate_limit)])
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    service.register_user(db, user_in)
    return {"message": "User created"}

@router.post("/login", response_model=Token, dependencies=[Depends(check_rate_limit)])
def login(user_in: UserLogin, db: Session = Depends(get_db)):
    return service.authenticate_user(db, user_in)
