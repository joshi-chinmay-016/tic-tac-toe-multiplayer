import re

with open("app/games/websocket.py", "r") as f:
    content = f.read()

new_check_timeout = """
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
"""

# Find the start and end of check_timeout
start_idx = content.find("    async def check_timeout():")
if start_idx != -1:
    # Find the end of check_timeout, which is where timer_task is defined
    end_idx = content.find("    if not is_spectator and match.status == \"active\":", start_idx)

    if end_idx != -1:
        content = content[:start_idx] + new_check_timeout.strip('\n') + "\n\n" + content[end_idx:]

# Replace 'last_move_time = time.time()' with Redis updates
content = content.replace("last_move_time = time.time()", "await redis_client.set(f'game:{match_id}:last_move', str(time.time()))")

# Remove nonlocal last_move_time
content = content.replace("nonlocal last_move_time", "")
content = content.replace("last_move_time = time.time()", "")
content = content.replace("timer_task = None", "timer_task = None\n    await redis_client.set(f'game:{match_id}:last_move', str(time.time()))")

with open("app/games/websocket.py", "w") as f:
    f.write(content)
