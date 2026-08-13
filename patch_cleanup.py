import re

with open("app/games/websocket.py", "r") as f:
    content = f.read()

# 1. Clean up duplicate imports at the top
import_block1 = "from app.api.dependencies import get_current_user\\nfrom app.models.user import User\\n"
import_block2 = "from app.api.dependencies import get_current_user\\nfrom app.models.user import User"
while content.startswith("from app.api.dependencies import get_current_user\nfrom app.models.user import User\nfrom app.api.dependencies import get_current_user\nfrom app.models.user import User"):
    content = content.replace("from app.api.dependencies import get_current_user\nfrom app.models.user import User\nfrom app.api.dependencies import get_current_user\nfrom app.models.user import User", "from app.api.dependencies import get_current_user\nfrom app.models.user import User", 1)

# 2. Clean up duplicated AI start logic
ai_start_logic_regex = r'(    # Check if AI should make the first move\n    if match.game_type == "vs_ai" and match.status == "active" and not is_spectator:.*?await manager.broadcast\(match_id, \{.*?"turn_timer": TURN_TIMEOUT_SECONDS\n            \}\)\n)'
matches = list(re.finditer(ai_start_logic_regex, content, re.DOTALL))
if len(matches) > 1:
    # Keep the first one, remove the rest
    first_match = matches[0].group(1)
    content = re.sub(ai_start_logic_regex, "", content, flags=re.DOTALL)

    target_str = 'await manager.broadcast(match_id, {"type": "opponent_reconnected" if match.status == "active" else "player_joined"})'
    content = content.replace(target_str, target_str + "\n\n" + first_match, 1)

with open("app/games/websocket.py", "w") as f:
    f.write(content)
