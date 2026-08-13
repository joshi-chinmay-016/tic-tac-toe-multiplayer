import re

with open("app/games/websocket.py", "r") as f:
    content = f.read()

ai_start_logic_regex = r'(    # Check if AI should make the first move\n    if match.game_type == "vs_ai" and match.status == "active" and not is_spectator:.*?await manager.broadcast\(match_id, \{.*?"turn_timer": TURN_TIMEOUT_SECONDS\n            \}\)\n)'
content = re.sub(ai_start_logic_regex, "", content, flags=re.DOTALL)

with open("app/games/websocket.py", "w") as f:
    f.write(content)
