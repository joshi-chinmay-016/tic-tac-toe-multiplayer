from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

from app.database.base import Base
from app.database.session import engine
from app.models.user import User
from app.models.game import Game

from app.auth.router import router as auth_router
from app.matchmaking.router import router as matchmaking_router
from app.games.websocket import router as ws_router
from app.games.router import router as game_router
from app.leaderboard.router import router as leaderboard_router
from app.rooms.router import router as rooms_router
from app.users.router import router as users_router

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

app.include_router(auth_router)
app.include_router(matchmaking_router)
app.include_router(ws_router)
app.include_router(game_router)
app.include_router(leaderboard_router)
app.include_router(rooms_router)
app.include_router(users_router)

# ─── Serve frontend ───
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")

if os.path.isdir(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

    @app.get("/")
    def serve_index():
        return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))
else:
    @app.get("/")
    def root():
        return {"message": "Tic Tac Toe Backend is running 🚀"}