import json
import time
from app.redis.client import redis_client

MATCHMAKING_QUEUE_KEY = "matchmaking:queue"
MATCHMAKING_PENDING_KEY = "matchmaking:pending"

async def add_to_queue(user_id: int):
    await redis_client.zadd(MATCHMAKING_QUEUE_KEY, {str(user_id): time.time()})

async def remove_from_queue(user_id: int):
    await redis_client.zrem(MATCHMAKING_QUEUE_KEY, str(user_id))

async def check_pending_match(user_id: int):
    pending_match = await redis_client.hget(MATCHMAKING_PENDING_KEY, str(user_id))
    if pending_match:
        await redis_client.hdel(MATCHMAKING_PENDING_KEY, str(user_id))
        return json.loads(pending_match)
    return None

async def find_match():
    players = await redis_client.zrange(MATCHMAKING_QUEUE_KEY, 0, 1)
    if len(players) >= 2:
        player_1, player_2 = players
        removed_count = await redis_client.zrem(MATCHMAKING_QUEUE_KEY, player_1, player_2)
        if removed_count == 2:
            return int(player_1), int(player_2)
    return None

async def set_pending_match(user_id: int, match_data: dict):
    await redis_client.hset(MATCHMAKING_PENDING_KEY, str(user_id), json.dumps(match_data))
