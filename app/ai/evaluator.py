from app.ai.minimax import MinimaxAI
from app.ai.base import AIPlayer
import time

class ImpossibleAI(AIPlayer):
    def __init__(self):
        self.minimax_engine = MinimaxAI()

    def get_move_with_stats(self, board: list[str], ai_symbol: str, opponent_symbol: str) -> dict:
        start_time = time.perf_counter()
        move = self.minimax_engine.get_move(board, ai_symbol, opponent_symbol)
        end_time = time.perf_counter()

        return {
            "move": move,
            "difficulty": "impossible",
            "algorithm": "minimax-alpha-beta",
            "nodes_evaluated": self.minimax_engine.nodes_evaluated,
            "decision_time_ms": round((end_time - start_time) * 1000, 2)
        }

    def get_move(self, board: list[str], ai_symbol: str, opponent_symbol: str) -> int:
        return self.minimax_engine.get_move(board, ai_symbol, opponent_symbol)
