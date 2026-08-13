from app.api.dependencies import get_current_user
from app.models.user import User
from app.models.user import User
from app.api.dependencies import get_current_user
from fastapi import Depends
from app.database.session import get_db
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from app.database.session import SessionLocal
from app.models.game import Game
from app.models.game_event import GameEvent
from app.models.user import User
from app.games.engine import GameEngine
from app.games.service import GameService
from app.redis.client import redis_client
from app.websocket.manager import ConnectionManager
from app.core.config import settings
import asyncio
import time

router = APIRouter()
manager = ConnectionManager()

def get_user_from_token(token: str) -> int:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        return int(user_id)
    except JWTError:
        return None

TURN_TIMEOUT_SECONDS = 30

@router.websocket("/ws/game/{match_id}")
async def websocket_game(websocket: WebSocket, match_id: int, token: str):
    user_id = get_user_from_token(token)
    if not user_id:
        await websocket.close(code=1008)
        return

    db = SessionLocal()
    match = db.query(Game).filter(Game.id == match_id).first()

    if not match:
        await websocket.close(code=1008)
        db.close()
        return

    is_spectator = user_id not in (match.player_x_id, match.player_o_id)

    await manager.connect(match_id, user_id, websocket, is_spectator)

    state_msg = {
        "type": "game_state",
        "game_id": match.id,
        "board": match.board_state,
        "current_turn": match.current_turn,
        "status": match.status,
        "winner": match.winner,
        "winning_line": match.winning_line,
        "version": match.move_count,
        "turn_timer": TURN_TIMEOUT_SECONDS
    }
    await manager.send_personal_message(state_msg, match_id, user_id)

    if not is_spectator:
        await manager.broadcast(match_id, {"type": "opponent_reconnected" if match.status == "active" else "player_joined"})

    # Check if AI should make the first move
    if match.game_type == "vs_ai" and match.status == "active" and not is_spectator:
        my_symbol = "X" if match.player_x_id == user_id else "O"
        ai_symbol = "O" if my_symbol == "X" else "X"
        if match.current_turn == ai_symbol and match.move_count == 0:
            # It's the AI's turn to start!
            await asyncio.sleep(0.5)
            db.refresh(match)
            ai_move = GameService.get_ai_move(match.board_state, match.ai_difficulty, ai_symbol, my_symbol)
            new_board = GameEngine.apply_move(match.board_state, ai_move, ai_symbol)
            match.board_state = new_board
            match.move_count += 1
            await redis_client.set(f'game:{match_id}:last_move', str(time.time()))
            event = GameEvent(game_id=match.id, player_id=None, symbol=ai_symbol, position=ai_move, move_number=match.move_count)
            db.add(event)
            match.current_turn = GameEngine.switch_turn(match.current_turn)
            db.commit()
            await manager.broadcast(match_id, {
                "type": "game_state",
                "game_id": match.id,
                "board": match.board_state,
                "current_turn": match.current_turn,
                "status": match.status,
                "winner": match.winner,
                "winning_line": match.winning_line,
                "version": match.move_count,
                "turn_timer": TURN_TIMEOUT_SECONDS
            })


    # Check if AI should make the first move

    if match.game_type == "vs_ai" and match.status == "active" and not is_spectator:
        my_symbol = "X" if match.player_x_id == user_id else "O"
        ai_symbol = "O" if my_symbol == "X" else "X"
        if match.current_turn == ai_symbol and match.move_count == 0:
            # It's the AI's turn to start!
            await asyncio.sleep(0.5)
            db.refresh(match)
            ai_move = GameService.get_ai_move(match.board_state, match.ai_difficulty, ai_symbol, my_symbol)
            new_board = GameEngine.apply_move(match.board_state, ai_move, ai_symbol)
            match.board_state = new_board
            match.move_count += 1
            await redis_client.set(f'game:{match_id}:last_move', str(time.time()))
            event = GameEvent(game_id=match.id, player_id=None, symbol=ai_symbol, position=ai_move, move_number=match.move_count)
            db.add(event)
            match.current_turn = GameEngine.switch_turn(match.current_turn)
            db.commit()
            await manager.broadcast(match_id, {
                "type": "game_state",
                "game_id": match.id,
                "board": match.board_state,
                "current_turn": match.current_turn,
                "status": match.status,
                "winner": match.winner,
                "winning_line": match.winning_line,
                "version": match.move_count,
                "turn_timer": TURN_TIMEOUT_SECONDS
            })


    # Check if AI should make the first move

    if match.game_type == "vs_ai" and match.status == "active" and not is_spectator:
        my_symbol = "X" if match.player_x_id == user_id else "O"
        ai_symbol = "O" if my_symbol == "X" else "X"
        if match.current_turn == ai_symbol and match.move_count == 0:
            # It's the AI's turn to start!
            await asyncio.sleep(0.5)
            db.refresh(match)
            ai_move = GameService.get_ai_move(match.board_state, match.ai_difficulty, ai_symbol, my_symbol)
            new_board = GameEngine.apply_move(match.board_state, ai_move, ai_symbol)
            match.board_state = new_board
            match.move_count += 1
            await redis_client.set(f'game:{match_id}:last_move', str(time.time()))
            event = GameEvent(game_id=match.id, player_id=None, symbol=ai_symbol, position=ai_move, move_number=match.move_count)
            db.add(event)
            match.current_turn = GameEngine.switch_turn(match.current_turn)
            db.commit()
            await manager.broadcast(match_id, {
                "type": "game_state",
                "game_id": match.id,
                "board": match.board_state,
                "current_turn": match.current_turn,
                "status": match.status,
                "winner": match.winner,
                "winning_line": match.winning_line,
                "version": match.move_count,
                "turn_timer": TURN_TIMEOUT_SECONDS
            })


    # Check if AI should make the first move

    if match.game_type == "vs_ai" and match.status == "active" and not is_spectator:
        my_symbol = "X" if match.player_x_id == user_id else "O"
        ai_symbol = "O" if my_symbol == "X" else "X"
        if match.current_turn == ai_symbol and match.move_count == 0:
            # It's the AI's turn to start!
            await asyncio.sleep(0.5)
            db.refresh(match)
            ai_move = GameService.get_ai_move(match.board_state, match.ai_difficulty, ai_symbol, my_symbol)
            new_board = GameEngine.apply_move(match.board_state, ai_move, ai_symbol)
            match.board_state = new_board
            match.move_count += 1
            await redis_client.set(f'game:{match_id}:last_move', str(time.time()))
            event = GameEvent(game_id=match.id, player_id=None, symbol=ai_symbol, position=ai_move, move_number=match.move_count)
            db.add(event)
            match.current_turn = GameEngine.switch_turn(match.current_turn)
            db.commit()
            await manager.broadcast(match_id, {
                "type": "game_state",
                "game_id": match.id,
                "board": match.board_state,
                "current_turn": match.current_turn,
                "status": match.status,
                "winner": match.winner,
                "winning_line": match.winning_line,
                "version": match.move_count,
                "turn_timer": TURN_TIMEOUT_SECONDS
            })


    # Track time for this connection. Realistically, timer should be a background asyncio task tied to the match_id,
    # but for simplicity, we embed the logic in the receive loop or we can just pass the responsibility to the client
    # to enforce their own timeout and have server validate. Let's create an async task for timeout.

    timer_task = None
    await redis_client.set(f'game:{match_id}:last_move', str(time.time()))

    async def check_timeout():
        while True:
            await asyncio.sleep(1)

            db_local = SessionLocal()
            match_local = db_local.query(Game).filter(Game.id == match_id).first()
            if not match_local or match_local.status != "active":
                db_local.close()
                break

            # Get last move time from Redis
            last_move_key = f"game:{match_id}:last_move"
            last_time_str = await redis_client.get(last_move_key)

            if not last_time_str:
                # Initialize it
                await redis_client.set(last_move_key, str(time.time()))
                db_local.close()
                continue

            last_time = float(last_time_str)

            if time.time() - last_time > TURN_TIMEOUT_SECONDS:
                # Turn expired, current player forfeits the game
                match_local.status = "completed"
                match_local.winner = "O" if match_local.current_turn == "X" else "X"
                match_local.completed_at = time.strftime('%Y-%m-%d %H:%M:%S')
                db_local.commit()

                await manager.broadcast(match_id, {
                    "type": "game_state",
                    "game_id": match_local.id,
                    "board": match_local.board_state,
                    "current_turn": match_local.current_turn,
                    "status": match_local.status,
                    "winner": match_local.winner,
                    "winning_line": None,
                    "version": match_local.move_count,
                    "message": "Time expired. Player forfeits."
                })
                db_local.close()
                break
            db_local.close()

    if not is_spectator and match.status == "active":
        timer_task = asyncio.create_task(check_timeout())

    try:
        while True:
            data = await websocket.receive_json()
            msg_type = data.get("type")

            db.refresh(match)

            if msg_type == "rematch_request":
                if is_spectator or match.status != "completed":
                    continue

                other_player_id = match.player_o_id if user_id == match.player_x_id else match.player_x_id

                # Use Redis to store the request state
                key = f"rematch:{match.id}"
                await redis_client.hset(key, str(user_id), "requested")
                await redis_client.expire(key, 60) # 1 min to accept

                # Check if both requested
                state = await redis_client.hgetall(key)
                if str(match.player_x_id) in state and str(match.player_o_id) in state:
                    # Create rematch
                    new_game = GameService.create_rematch(db, match)
                    await manager.broadcast(match_id, {
                        "type": "rematch_accepted",
                        "new_match_id": new_game.id
                    })
                else:
                    await manager.broadcast(match_id, {
                        "type": "rematch_requested",
                        "requested_by": user_id
                    })
                continue

            if msg_type == "rematch_decline":
                if is_spectator or match.status != "completed":
                    continue
                await manager.broadcast(match_id, {
                    "type": "rematch_declined",
                    "declined_by": user_id
                })
                continue

            if msg_type == "move":
                if is_spectator:
                    await manager.send_personal_message({"type": "error", "error": {"code": "SPECTATOR", "message": "Spectators cannot move."}}, match_id, user_id)
                    continue

                if match.status != "active":
                    await manager.send_personal_message({"type": "error", "error": {"code": "GAME_OVER", "message": "Game is already completed."}}, match_id, user_id)
                    continue

                position = data.get("position")
                my_symbol = "X" if match.player_x_id == user_id else "O"

                if match.current_turn != my_symbol:
                    await manager.send_personal_message({"type": "error", "error": {"code": "WRONG_TURN", "message": "It is not your turn."}}, match_id, user_id)
                    continue

                try:
                    new_board = GameEngine.apply_move(match.board_state, position, my_symbol)
                except ValueError as e:
                    await manager.send_personal_message({"type": "error", "error": {"code": "INVALID_MOVE", "message": str(e)}}, match_id, user_id)
                    continue

                match.board_state = new_board
                match.move_count += 1
                await redis_client.set(f'game:{match_id}:last_move', str(time.time()))  # Reset timer

                event = GameEvent(game_id=match.id, player_id=user_id, symbol=my_symbol, position=position, move_number=match.move_count)
                db.add(event)

                winner = GameEngine.check_winner(new_board)
                if winner:
                    match.winning_line = GameEngine.get_winning_line(new_board)
                    match.completed_at = time.strftime('%Y-%m-%d %H:%M:%S')
                    db.commit()
                    GameService.finalize_game(db, match, winner)
                elif GameEngine.is_draw(new_board):
                    match.completed_at = time.strftime('%Y-%m-%d %H:%M:%S')
                    db.commit()
                    GameService.finalize_game(db, match, "draw")
                else:
                    match.current_turn = GameEngine.switch_turn(match.current_turn)
                    db.commit()

                await manager.broadcast(match_id, {
                    "type": "game_state",
                    "game_id": match.id,
                    "board": match.board_state,
                    "current_turn": match.current_turn,
                    "status": match.status,
                    "winner": match.winner,
                    "winning_line": match.winning_line,
                    "version": match.move_count,
                    "turn_timer": TURN_TIMEOUT_SECONDS
                })

                if match.game_type == "vs_ai" and match.status == "active":
                    ai_symbol = "O" if my_symbol == "X" else "X"
                    await asyncio.sleep(0.5)

                    db.refresh(match)
                    ai_move = GameService.get_ai_move(match.board_state, match.ai_difficulty, ai_symbol, my_symbol)

                    new_board = GameEngine.apply_move(match.board_state, ai_move, ai_symbol)
                    match.board_state = new_board
                    match.move_count += 1
                    await redis_client.set(f'game:{match_id}:last_move', str(time.time())) # Reset timer again

                    event = GameEvent(game_id=match.id, player_id=None, symbol=ai_symbol, position=ai_move, move_number=match.move_count)
                    db.add(event)

                    winner = GameEngine.check_winner(new_board)
                    if winner:
                        match.winning_line = GameEngine.get_winning_line(new_board)
                        match.completed_at = time.strftime('%Y-%m-%d %H:%M:%S')
                        db.commit()
                        GameService.finalize_game(db, match, winner)
                    elif GameEngine.is_draw(new_board):
                        match.completed_at = time.strftime('%Y-%m-%d %H:%M:%S')
                        db.commit()
                        GameService.finalize_game(db, match, "draw")
                    else:
                        match.current_turn = GameEngine.switch_turn(match.current_turn)
                        db.commit()

                    await manager.broadcast(match_id, {
                        "type": "game_state",
                        "game_id": match.id,
                        "board": match.board_state,
                        "current_turn": match.current_turn,
                        "status": match.status,
                        "winner": match.winner,
                        "winning_line": match.winning_line,
                        "version": match.move_count,
                        "turn_timer": TURN_TIMEOUT_SECONDS
                    })

    except WebSocketDisconnect:
        manager.disconnect(match_id, user_id, websocket)
        if not is_spectator:
            await manager.broadcast(match_id, {"type": "opponent_disconnected"})
    finally:
        if timer_task:
            timer_task.cancel()
        db.close()

@router.post("/games/ai")
async def start_ai_game(
    difficulty: str,
    symbol: str,
    starts: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    game = GameService.create_ai_game(db, current_user.id, difficulty, symbol, starts)
    # If AI starts, we need to apply its first move immediately, or let the websocket handle it
    # Easiest way is to just let the websocket handling see it's AI turn and make the move.
    return {"match_id": game.id, "message": "AI game created"}
