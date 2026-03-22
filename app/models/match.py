from sqlalchemy import Column, Integer, String
from app.database import Base

class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)

    player_x = Column(Integer)
    player_o = Column(Integer)

    board_state = Column(String, default=",".join([""] * 9))
    status = Column(String, default="waiting")
    winner = Column(String, nullable=True)
