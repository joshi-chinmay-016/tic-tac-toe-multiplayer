import random
from typing import List
from app.ai.base import AIPlayer
from app.games.engine import GameEngine

class MediumAI(AIPlayer):
    def __init__(self, seed: int = None):
        if seed is not None:
            random.seed(seed)

    def get_move(self, board: List[str], ai_symbol: str, opponent_symbol: str) -> int:
        valid_moves = GameEngine.get_valid_moves(board)
        if not valid_moves:
            raise ValueError("No valid moves available")

        for move in valid_moves:
            simulated_board = list(board)
            simulated_board[move] = ai_symbol
            if GameEngine.check_winner(simulated_board) == ai_symbol:
                return move

        for move in valid_moves:
            simulated_board = list(board)
            simulated_board[move] = opponent_symbol
            if GameEngine.check_winner(simulated_board) == opponent_symbol:
                return move

        if 4 in valid_moves:
            return 4

        corners = [m for m in [0, 2, 6, 8] if m in valid_moves]
        if corners:
            return random.choice(corners)

        return random.choice(valid_moves)
