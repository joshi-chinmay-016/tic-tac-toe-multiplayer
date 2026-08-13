import asyncio
import httpx

async def test_rate_limit():
    async with httpx.AsyncClient() as client:
        # Our limit is 20 requests per 10 seconds. We'll send 25 quickly.
        tasks = []
        for _ in range(25):
            tasks.append(client.post("http://127.0.0.1:8000/auth/register", json={"username": "rl_user", "password": "password1"}))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        status_codes = []
        for res in results:
            if not isinstance(res, Exception):
                status_codes.append(res.status_code)

        print("Status codes received:", set(status_codes))
        if 429 in status_codes:
            print("Rate limiting confirmed: 429 Too Many Requests received.")
        else:
            print("Rate limiting failed to trigger!")

if __name__ == "__main__":
    asyncio.run(test_rate_limit())
