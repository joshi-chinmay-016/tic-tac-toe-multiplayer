import pytest
from app.games.engine import GameEngine

def test_get_valid_moves():
    board = ["X", "", "O", "", "X", "", "", "", "O"]
    moves = GameEngine.get_valid_moves(board)
    assert moves == [1, 3, 5, 6, 7]

def test_check_winner_horizontal():
    board = ["X", "X", "X", "", "O", "", "O", "", ""]
    assert GameEngine.check_winner(board) == "X"

def test_check_winner_vertical():
    board = ["O", "X", "", "O", "", "", "O", "X", "X"]
    assert GameEngine.check_winner(board) == "O"

def test_check_winner_diagonal():
    board = ["X", "O", "", "", "X", "", "O", "", "X"]
    assert GameEngine.check_winner(board) == "X"

def test_is_draw():
    board = ["X", "O", "X", "X", "O", "O", "O", "X", "X"]
    assert GameEngine.is_draw(board) == True
    assert GameEngine.check_winner(board) is None

def test_is_not_draw_if_winner():
    board = ["X", "O", "X", "X", "O", "O", "X", "X", "O"]
    assert GameEngine.check_winner(board) == "X"
    assert GameEngine.is_draw(board) == False

def test_apply_move_valid():
    board = ["", "", "", "", "", "", "", "", ""]
    new_board = GameEngine.apply_move(board, 4, "X")
    assert new_board[4] == "X"
    assert board[4] == "" # Immutability check

def test_apply_move_invalid_occupied():
    board = ["X", "", "", "", "", "", "", "", ""]
    with pytest.raises(ValueError):
        GameEngine.apply_move(board, 0, "O")

def test_apply_move_invalid_out_of_bounds():
    board = ["", "", "", "", "", "", "", "", ""]
    with pytest.raises(ValueError):
        GameEngine.apply_move(board, 9, "X")
    with pytest.raises(ValueError):
        GameEngine.apply_move(board, -1, "X")

def test_switch_turn():
    assert GameEngine.switch_turn("X") == "O"
    assert GameEngine.switch_turn("O") == "X"
