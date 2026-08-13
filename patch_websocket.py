def run():
    with open("app/games/websocket.py", "r") as f:
        content = f.read()

    # We want to add a check for the AI starting right after "await manager.broadcast(match_id, {"type": "opponent_reconnected" if match.status == "active" else "player_joined"})"

    ai_start_logic = """
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
            last_move_time = time.time()
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
    """

    target_str = 'await manager.broadcast(match_id, {"type": "opponent_reconnected" if match.status == "active" else "player_joined"})'
    content = content.replace(target_str, target_str + "\n\n    # Check if AI should make the first move\n" + ai_start_logic)

    with open("app/games/websocket.py", "w") as f:
        f.write(content)

run()
