from backend import db
from backend import api
from datetime import datetime
import time 


def sync_user(steam_id):

    user_info = api.get_user_info(steam_id)
    steam_name = user_info["response"]["players"][0]["personaname"]
    db.upsert_user(steam_id, steam_name, None)
    owned_games = api.get_owned_games(steam_id)
    
    for game in owned_games.get("played_games", []):
        app_id, game_name = game[0], game[1]
        db.upsert_user_game(steam_id,app_id)
        db.upsert_game(app_id, game_name)
        
        game_info = api.get_game_stats(app_id)
        player_info = api.get_achievements_for_player(steam_id, app_id)
        
        if game_info is None or player_info is None:
            continue
        
        player_stats = player_info.get("playerstats") or {}
        player_achievements = player_stats.get("achievements") or []
        game_stats = game_info.get("availableGameStats") or {}
        game_achievements = game_stats.get("achievements") or []
        
        for achievement in game_achievements:
            db.upsert_achievement(
                app_id,
                achievement.get("name"),
                achievement.get("displayName"),
                achievement.get("description"),
                achievement.get("icon")
            )
        
        for achievement in player_achievements:
            if achievement.get("achieved") == 1:
                db.upsert_user_achievement(
                    steam_id,
                    app_id,
                    achievement.get("apiname"),
                    achievement.get("unlocktime")
                )

    db.update_sync(steam_id, int(time.time()))

