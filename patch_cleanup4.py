import re

with open("app/games/websocket.py", "r") as f:
    content = f.read()

content = content.replace("    await redis_client.set(f'game:{match_id}:last_move', str(time.time()))\n    await redis_client.set(f'game:{match_id}:last_move', str(time.time()))", "    await redis_client.set(f'game:{match_id}:last_move', str(time.time()))")

content = re.sub(r'    current_user: User = Depends\(get_current_user\)\n\n\n\n\n\):', '    current_user: User = Depends(get_current_user)\n):', content)

with open("app/games/websocket.py", "w") as f:
    f.write(content)
