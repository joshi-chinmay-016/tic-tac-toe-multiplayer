WIN_PATTERNS = [
    (0,1,2),(3,4,5),(6,7,8),
    (0,3,6),(1,4,7),(2,5,8),
    (0,4,8),(2,4,6)
]

def check_winner(board):
    for a,b,c in WIN_PATTERNS:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    if "" not in board:
        return "draw"
    return None
