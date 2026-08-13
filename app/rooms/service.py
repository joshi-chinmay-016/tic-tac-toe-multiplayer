from sqlalchemy.orm import Session
from app.models.game import Game
import random
import string
import json
from app.redis.client import redis_client

ROOMS_KEY_PREFIX = "room:"

async def create_room(db: Session, host_id: int) -> str:
    # Generate unique short code
    while True:
        code = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        exists = await redis_client.exists(f"{ROOMS_KEY_PREFIX}{code}")
        if not exists:
            break

    room_data = {
        "host_id": host_id,
        "player_o_id": None,
        "status": "waiting",
        "game_id": None
    }

    # expire room after 1 hour if not started
    await redis_client.setex(f"{ROOMS_KEY_PREFIX}{code}", 3600, json.dumps(room_data))
    return code

async def join_room(db: Session, code: str, user_id: int) -> dict:
    room_key = f"{ROOMS_KEY_PREFIX}{code}"
    room_json = await redis_client.get(room_key)
    if not room_json:
        return {"error": "Room not found or expired"}

    room_data = json.loads(room_json)

    if room_data["host_id"] == user_id:
        # Check if game already started
        if room_data["game_id"]:
            return {"match_id": room_data["game_id"], "player_x": room_data["host_id"], "player_o": room_data["player_o_id"]}
        return {"message": "Waiting for opponent", "code": code}

    if room_data["status"] == "waiting":
        room_data["player_o_id"] = user_id
        room_data["status"] = "active"

        # Create game in DB
        new_game = Game(
            game_type="private",
            player_x_id=room_data["host_id"],
            player_o_id=user_id,
            status="active"
        )
        db.add(new_game)
        db.commit()
        db.refresh(new_game)

        room_data["game_id"] = new_game.id
        await redis_client.setex(room_key, 3600, json.dumps(room_data))

        return {
            "match_id": new_game.id,
            "player_x": room_data["host_id"],
            "player_o": user_id
        }

    elif room_data["status"] == "active":
        if room_data["player_o_id"] == user_id:
            return {
                "match_id": room_data["game_id"],
                "player_x": room_data["host_id"],
                "player_o": user_id
            }
        else:
            return {"error": "Room is full"}

    return {"error": "Unknown room state"}
