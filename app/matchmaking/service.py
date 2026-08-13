from sqlalchemy.orm import Session
from app.models.game import Game
from app.redis import matchmaking

async def process_matchmaking(db: Session, user_id: int):
    pending = await matchmaking.check_pending_match(user_id)
    if pending:
        return pending

    await matchmaking.add_to_queue(user_id)

    match_players = await matchmaking.find_match()
    if match_players:
        player_x, player_o = match_players

        new_game = Game(
            game_type="multiplayer",
            player_x_id=player_x,
            player_o_id=player_o,
            status="active"
        )
        db.add(new_game)
        db.commit()
        db.refresh(new_game)

        match_info = {
            "match_id": new_game.id,
            "player_x": player_x,
            "player_o": player_o
        }

        other_player = player_o if user_id == player_x else player_x
        await matchmaking.set_pending_match(other_player, match_info)

        return match_info

    return None
