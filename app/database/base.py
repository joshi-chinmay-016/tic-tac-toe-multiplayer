from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from app.models.user import User
from app.models.game import Game
from app.models.game_event import GameEvent
from app.models.refresh_token import RefreshToken
