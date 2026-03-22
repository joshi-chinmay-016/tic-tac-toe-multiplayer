from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.database import SessionLocal
from app.models.match import Match
from app.models.user import User
from app.game.engine import check_winner
from app.game.websocket_manager import ConnectionManager

router = APIRouter()
manager = ConnectionManager()

@router.websocket("/ws/game/{match_id}")
async def websocket_game(websocket: WebSocket, match_id: int):

    await manager.connect(match_id, websocket)

    try:
        while True:

            data = await websocket.receive_json()
            position = data["position"]

            db = SessionLocal()
            match = db.query(Match).filter(Match.id == match_id).first()

            if not match:
                await websocket.close()
                return

            board = match.board_state.split(",")

            if match.status == "finished":
                db.close()
                continue

            if board[position] != "":
                db.close()
                continue

            turn = "X" if board.count("X") <= board.count("O") else "O"

            board[position] = turn
            match.board_state = ",".join(board)

            winner = check_winner(board)

            if winner:
                match.status = "finished"
                match.winner = winner

                user_x = db.query(User).filter(User.id == match.player_x).first()
                user_o = db.query(User).filter(User.id == match.player_o).first()

                if user_x and user_o:
                    if winner == "X":
                        user_x.wins += 1
                        user_o.losses += 1
                    elif winner == "O":
                        user_o.wins += 1
                        user_x.losses += 1

            db.commit()

            await manager.broadcast(match_id, {
                "board": board,
                "winner": winner
            })

            db.close()

    except WebSocketDisconnect:
        manager.disconnect(match_id, websocket)
