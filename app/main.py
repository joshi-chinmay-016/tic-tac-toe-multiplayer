from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.models.user import User
from app.models.match import Match

from app.auth.routes import router as auth_router
from app.matchmaking.routes import router as matchmaking_router
from app.game.routes import router as game_router
from app.leaderboard.routes import router as leaderboard_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Tic Tac Toe Arena",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Tic Tac Toe Backend is running 🚀"}


app.include_router(auth_router)
app.include_router(matchmaking_router)
app.include_router(game_router)
app.include_router(leaderboard_router)