from fastapi import Request, HTTPException
import time
from app.redis.client import redis_client

async def check_rate_limit(request: Request):
    client_ip = request.client.host
    endpoint = request.url.path

    # 20 requests per 10 seconds per IP
    limit = 20
    window = 10

    key = f"ratelimit:{client_ip}:{endpoint}"
    current_time = int(time.time())

    # Simple fixed window counter using Redis
    async with redis_client.pipeline(transaction=True) as pipe:
        pipe.incr(key)
        pipe.expire(key, window)
        results = await pipe.execute()

    count = results[0]
    if count > limit:
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Please try again later.")
