from typing import List
from app.ai.base import AIPlayer
from app.games.engine import GameEngine

class MinimaxAI(AIPlayer):
    def __init__(self):
        self.nodes_evaluated = 0

    def get_move(self, board: List[str], ai_symbol: str, opponent_symbol: str) -> int:
        self.nodes_evaluated = 0

        valid_moves = GameEngine.get_valid_moves(board)
        if not valid_moves:
            raise ValueError("No valid moves available")

        best_score = -float('inf')
        best_move = valid_moves[0]

        alpha = -float('inf')
        beta = float('inf')

        for move in valid_moves:
            b = list(board)
            b[move] = ai_symbol
            score = self.minimax(b, False, alpha, beta, ai_symbol, opponent_symbol, 0)
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, best_score)

        return best_move

    def minimax(self, board: List[str], is_maximizing: bool, alpha: float, beta: float, ai_symbol: str, opponent_symbol: str, depth: int) -> int:
        self.nodes_evaluated += 1

        winner = GameEngine.check_winner(board)
        if winner == ai_symbol:
            return 10 - depth
        elif winner == opponent_symbol:
            return -10 + depth
        elif GameEngine.is_draw(board):
            return 0

        valid_moves = GameEngine.get_valid_moves(board)

        if is_maximizing:
            max_eval = -float('inf')
            for move in valid_moves:
                b = list(board)
                b[move] = ai_symbol
                ev = self.minimax(b, False, alpha, beta, ai_symbol, opponent_symbol, depth + 1)
                max_eval = max(max_eval, ev)
                alpha = max(alpha, ev)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in valid_moves:
                b = list(board)
                b[move] = opponent_symbol
                ev = self.minimax(b, True, alpha, beta, ai_symbol, opponent_symbol, depth + 1)
                min_eval = min(min_eval, ev)
                beta = min(beta, ev)
                if beta <= alpha:
                    break
            return min_eval
