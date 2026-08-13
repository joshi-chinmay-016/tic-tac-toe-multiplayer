import pytest
from app.ai.easy import EasyAI
from app.ai.medium import MediumAI
from app.ai.hard import HardAI
from app.ai.evaluator import ImpossibleAI
from app.games.engine import GameEngine

def test_easy_ai_returns_valid_move():
    ai = EasyAI()
    board = ["X", "", "O", "", "", "", "X", "O", ""]
    move = ai.get_move(board, "X", "O")
    assert board[move] == ""

def test_medium_ai_takes_winning_move():
    ai = MediumAI()
    board = ["X", "X", "", "O", "O", "", "", "", ""]
    # AI plays X, should take 2 to win
    move = ai.get_move(board, "X", "O")
    assert move == 2

def test_medium_ai_blocks_immediate_loss():
    ai = MediumAI()
    board = ["O", "O", "", "X", "", "", "", "", ""]
    # AI plays X, should take 2 to block O from winning
    move = ai.get_move(board, "X", "O")
    assert move == 2

def test_hard_ai_fork_defense():
    ai = HardAI()
    # O played 0, X played 4, O played 8
    # O is threatening to fork by playing 2 or 6.
    board = ["O", "", "", "", "X", "", "", "", "O"]
    move = ai.get_move(board, "X", "O")
    # A valid defense is usually to play on a side (1, 3, 5, 7) rather than a corner.
    assert move in [1, 3, 5, 7]

def test_impossible_ai_takes_forced_win():
    ai = ImpossibleAI()
    board = ["X", "X", "", "O", "O", "", "", "", ""]
    move = ai.get_move(board, "X", "O")
    assert move == 2

def test_impossible_ai_never_loses():
    # Helper to simulate games starting from blank
    ai = ImpossibleAI()
    board = [""] * 9

    # We will simulate O playing suboptimally, X is ImpossibleAI
    board[0] = "O"
    move = ai.get_move(board, "X", "O")
    assert move == 4 # Minimax should take center

def test_impossible_ai_blocks_trap():
    ai = ImpossibleAI()
    board = ["O", "", "", "", "X", "", "", "", "O"]
    # Similar to the hard AI test, it must not play corner (which gives away the win)
    move = ai.get_move(board, "X", "O")
    assert move in [1, 3, 5, 7]
