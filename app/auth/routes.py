from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.schemas.user import UserCreate, UserLogin
from app.models.user import User
from app.utils.security import hash_password, verify_password

router = APIRouter(prefix="/auth")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="User exists")

    new_user = User(
        username=user.username,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()

    return {"message": "User created"}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    return {"message": "Login success", "user_id": db_user.id}
