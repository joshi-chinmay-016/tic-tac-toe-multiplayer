import re

with open("app/games/websocket.py", "r") as f:
    content = f.read()

# Check for extra check_timeout breaks and extra code
content = re.sub(r'                break\n            db_local\.close\(\)\n                break\n                \n            if time\.time\(\) - last_move_time > TURN_TIMEOUT_SECONDS:.*?\n            db_local\.close\(\)', '                break\n            db_local.close()', content, flags=re.DOTALL)

with open("app/games/websocket.py", "w") as f:
    f.write(content)
