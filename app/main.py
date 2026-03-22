from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

from app.database import Base, engine
from app.models.user import User
from app.models.match import Match
from app.auth.routes import router as auth_router
from app.matchmaking.routes import router as matchmaking_router
from app.game.routes import router as game_router
from app.leaderboard.routes import router as leaderboard_router


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Tic Tac Toe Arena", version="1.0.0")

# ─── CORS (allows frontend to talk to backend on same or different host) ───
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── API Routes ───
app.include_router(auth_router)
app.include_router(matchmaking_router)
app.include_router(game_router)
app.include_router(leaderboard_router)

# ─── Serve the frontend static files ───
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")

if os.path.isdir(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

    @app.get("/", response_class=FileResponse)
    def serve_index():
        return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

else:
    @app.get("/")
    def root():
        return {"status": "Tic Tac Toe Backend Running"}
