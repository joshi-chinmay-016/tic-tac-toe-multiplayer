from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from app.database.base import Base

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)

    game_type = Column(String, default="multiplayer")

    player_x_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    player_o_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    ai_difficulty = Column(String, nullable=True)

    status = Column(String, default="waiting")

    board_state = Column(JSON, default=lambda: [""] * 9)
    current_turn = Column(String, default="X")

    winner = Column(String, nullable=True)
    winning_line = Column(JSON, nullable=True)

    move_count = Column(Integer, default=0)

    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
