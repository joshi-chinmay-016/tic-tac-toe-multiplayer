from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.game import Game
from app.models.user import User
from app.games.engine import GameEngine
from app.ai.easy import EasyAI
from app.ai.medium import MediumAI
from app.ai.hard import HardAI
from app.ai.evaluator import ImpossibleAI

def update_rating(rating1: int, rating2: int, result: float, k_factor: int = 32) -> int:
    """ Calculate new rating using Elo formula. result is 1 for win, 0.5 for draw, 0 for loss """
    expected = 1 / (1 + 10 ** ((rating2 - rating1) / 400))
    return int(rating1 + k_factor * (result - expected))

class GameService:
    @staticmethod
    def create_rematch(db: Session, old_game: Game) -> Game:
        # Create a new game, swapping symbols
        new_game = Game(
            game_type=old_game.game_type,
            player_x_id=old_game.player_o_id,
            player_o_id=old_game.player_x_id,
            ai_difficulty=old_game.ai_difficulty,
            status="active"
        )
        db.add(new_game)
        db.commit()
        db.refresh(new_game)
        return new_game

    @staticmethod
    def finalize_game(db: Session, game: Game, winner_symbol: str):
        game.status = "completed"
        game.winner = winner_symbol

        user_x = db.query(User).filter(User.id == game.player_x_id).first() if game.player_x_id else None
        user_o = db.query(User).filter(User.id == game.player_o_id).first() if game.player_o_id else None

        # Update statistics if this is a multiplayer game and both users exist
        if game.game_type == "multiplayer" and user_x and user_o:
            user_x.games_played += 1
            user_o.games_played += 1

            if winner_symbol == "X":
                user_x.wins += 1
                user_o.losses += 1

                user_x.current_streak += 1
                if user_x.current_streak > user_x.best_streak:
                    user_x.best_streak = user_x.current_streak
                user_o.current_streak = 0

                # Rating update
                new_x_rating = update_rating(user_x.rating, user_o.rating, 1.0)
                new_o_rating = update_rating(user_o.rating, user_x.rating, 0.0)
                user_x.rating = new_x_rating
                user_o.rating = new_o_rating

            elif winner_symbol == "O":
                user_o.wins += 1
                user_x.losses += 1

                user_o.current_streak += 1
                if user_o.current_streak > user_o.best_streak:
                    user_o.best_streak = user_o.current_streak
                user_x.current_streak = 0

                # Rating update
                new_x_rating = update_rating(user_x.rating, user_o.rating, 0.0)
                new_o_rating = update_rating(user_o.rating, user_x.rating, 1.0)
                user_x.rating = new_x_rating
                user_o.rating = new_o_rating

            elif winner_symbol == "draw":
                user_x.draws += 1
                user_o.draws += 1

                user_x.current_streak = 0
                user_o.current_streak = 0

                # Rating update
                new_x_rating = update_rating(user_x.rating, user_o.rating, 0.5)
                new_o_rating = update_rating(user_o.rating, user_x.rating, 0.5)
                user_x.rating = new_x_rating
                user_o.rating = new_o_rating

        db.commit()

    @staticmethod
    def create_ai_game(db: Session, user_id: int, difficulty: str, symbol: str, starts: str) -> Game:
        player_x_id = user_id if symbol == "X" else None
        player_o_id = user_id if symbol == "O" else None

        game = Game(
            game_type="vs_ai",
            player_x_id=player_x_id,
            player_o_id=player_o_id,
            ai_difficulty=difficulty,
            status="active"
        )
        db.add(game)
        db.commit()
        db.refresh(game)

        return game

    @staticmethod
    def get_ai_move(board: List[str], difficulty: str, ai_symbol: str, opponent_symbol: str) -> int:
        if difficulty == "easy":
            ai = EasyAI()
        elif difficulty == "medium":
            ai = MediumAI()
        elif difficulty == "hard":
            ai = HardAI()
        elif difficulty == "impossible":
            ai = ImpossibleAI()
        else:
            raise ValueError(f"Unknown AI difficulty: {difficulty}")

        return ai.get_move(board, ai_symbol, opponent_symbol)
