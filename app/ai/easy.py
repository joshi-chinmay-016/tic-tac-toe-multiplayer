import random
from typing import List
from app.ai.base import AIPlayer
from app.games.engine import GameEngine

class EasyAI(AIPlayer):
    def __init__(self, seed: int = None):
        if seed is not None:
            random.seed(seed)

    def get_move(self, board: List[str], ai_symbol: str, opponent_symbol: str) -> int:
        valid_moves = GameEngine.get_valid_moves(board)
        if not valid_moves:
            raise ValueError("No valid moves available")
        return random.choice(valid_moves)
