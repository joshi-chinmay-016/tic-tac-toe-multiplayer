from typing import List, Optional

WIN_PATTERNS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6)
]

class GameEngine:
    @staticmethod
    def get_valid_moves(board: List[str]) -> List[int]:
        return [i for i, cell in enumerate(board) if cell == ""]

    @staticmethod
    def check_winner(board: List[str]) -> Optional[str]:
        for a, b, c in WIN_PATTERNS:
            if board[a] and board[a] == board[b] == board[c]:
                return board[a]
        return None

    @staticmethod
    def get_winning_line(board: List[str]) -> Optional[List[int]]:
        for a, b, c in WIN_PATTERNS:
            if board[a] and board[a] == board[b] == board[c]:
                return [a, b, c]
        return None

    @staticmethod
    def is_draw(board: List[str]) -> bool:
        return "" not in board and GameEngine.check_winner(board) is None

    @staticmethod
    def is_game_over(board: List[str]) -> bool:
        return GameEngine.check_winner(board) is not None or GameEngine.is_draw(board)

    @staticmethod
    def apply_move(board: List[str], position: int, symbol: str) -> List[str]:
        if position < 0 or position > 8 or board[position] != "":
            raise ValueError("Invalid move")
        new_board = list(board)
        new_board[position] = symbol
        return new_board

    @staticmethod
    def switch_turn(current_turn: str) -> str:
        return "O" if current_turn == "X" else "X"
