import random
from typing import List
from app.ai.base import AIPlayer
from app.games.engine import GameEngine

class HardAI(AIPlayer):
    def __init__(self, seed: int = None):
        if seed is not None:
            random.seed(seed)

    def get_move(self, board: List[str], ai_symbol: str, opponent_symbol: str) -> int:
        valid_moves = GameEngine.get_valid_moves(board)
        if not valid_moves:
            raise ValueError("No valid moves available")

        for move in valid_moves:
            b = list(board)
            b[move] = ai_symbol
            if GameEngine.check_winner(b) == ai_symbol:
                return move

        for move in valid_moves:
            b = list(board)
            b[move] = opponent_symbol
            if GameEngine.check_winner(b) == opponent_symbol:
                return move

        for move in valid_moves:
            b = list(board)
            b[move] = ai_symbol
            winning_moves_created = 0
            for next_move in GameEngine.get_valid_moves(b):
                b2 = list(b)
                b2[next_move] = ai_symbol
                if GameEngine.check_winner(b2) == ai_symbol:
                    winning_moves_created += 1
            if winning_moves_created >= 2:
                return move

        opponent_fork_moves = []
        for move in valid_moves:
            b = list(board)
            b[move] = opponent_symbol
            winning_moves_created = 0
            for next_move in GameEngine.get_valid_moves(b):
                b2 = list(b)
                b2[next_move] = opponent_symbol
                if GameEngine.check_winner(b2) == opponent_symbol:
                    winning_moves_created += 1
            if winning_moves_created >= 2:
                opponent_fork_moves.append(move)

        if opponent_fork_moves:
            # Simple defense for multiple opponent forks (e.g. opposite corners)
            # Try to force opponent to block rather than allowing them to take the fork
            for move in valid_moves:
                b = list(board)
                b[move] = ai_symbol
                winning_moves_created = 0
                for next_move in GameEngine.get_valid_moves(b):
                    b2 = list(b)
                    b2[next_move] = ai_symbol
                    if GameEngine.check_winner(b2) == ai_symbol:
                        winning_moves_created += 1
                if winning_moves_created == 1:
                    # If this move threatens a win, make sure opponent's forced response
                    # doesn't land on their fork square
                    # This is slightly complex to code heuristically.
                    # Instead, we just take an edge over a corner.
                    edges = [1, 3, 5, 7]
                    empty_edges = [e for e in edges if e in valid_moves]
                    if empty_edges:
                        return random.choice(empty_edges)
            return opponent_fork_moves[0]

        if 4 in valid_moves:
            return 4

        corners = [0, 2, 6, 8]
        opposite = {0: 8, 8: 0, 2: 6, 6: 2}
        for c in corners:
            if board[c] == opponent_symbol and opposite[c] in valid_moves:
                return opposite[c]

        empty_corners = [c for c in corners if c in valid_moves]
        if empty_corners:
            return random.choice(empty_corners)

        empty_sides = [s for s in [1, 3, 5, 7] if s in valid_moves]
        if empty_sides:
            return random.choice(empty_sides)

        return random.choice(valid_moves)
