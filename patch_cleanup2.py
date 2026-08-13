import re

with open("app/games/websocket.py", "r") as f:
    content = f.read()

# Fix the duplicate timer blocks
dup_block_regex = r'            db_local\.close\(\)\n                break\n                \n            if time\.time\(\) - last_time > TURN_TIMEOUT_SECONDS:.*?db_local\.close\(\)'
content = re.sub(dup_block_regex, "", content, flags=re.DOTALL)
content = re.sub(r'            db_local\.close\(\)\n                break\n                \n            if time\.time\(\) - last_move_time > TURN_TIMEOUT_SECONDS:.*?db_local\.close\(\)', "", content, flags=re.DOTALL)

with open("app/games/websocket.py", "w") as f:
    f.write(content)
