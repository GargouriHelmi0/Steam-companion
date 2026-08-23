from backend import db
from backend import api
from datetime import datetime
import time 
from concurrent.futures import ThreadPoolExecutor,as_completed

def get_game_info(game,steam_id):
    try :
        app_id = game[0]
        game_info = api.get_game_stats(app_id)
        player_info = api.get_achievements_for_player(steam_id, app_id)
        if game_info is None or player_info is None:
                    return None
        player_stats = player_info.get("playerstats") or {}
        player_achievements = player_stats.get("achievements") or []
        game_stats = game_info.get("availableGameStats") or {}
        game_achievements = game_stats.get("achievements") or []
        
        return {
            "app_id" : app_id,
            "steam_id" : steam_id,
            "game_name" : game[1],
            "player_achievements" : player_achievements,
            "game_achievements" : game_achievements
        }
    except Exception:
        return None

def sync_user(steam_id):
    
    user_info = api.get_user_info(steam_id)
    steam_name = user_info["response"]["players"][0]["personaname"]
    db.upsert_user(steam_id, steam_name, None)
    owned_games = api.get_owned_games(steam_id)
    results = []
    with ThreadPoolExecutor(max_workers=10) as executor :
        futures = []
        for game in owned_games.get("played_games", []):
            future = executor.submit(get_game_info,game,steam_id)
            futures.append(future)
        for future in as_completed(futures):
            result = future.result()
            if result is not None:
                results.append(result)
            
            
    for result in results:
        app_id = result["app_id"]
        game_name = result["game_name"]
        db.upsert_game(app_id, game_name)
        db.upsert_user_game(steam_id, app_id)

        for achievement in result["game_achievements"]:
            db.upsert_achievement(
                app_id,
                achievement.get("name"),
                achievement.get("displayName"),
                achievement.get("description"),
                achievement.get("icon")
            )
            

        for achievement in result["player_achievements"]:
            if achievement.get("achieved") == 1:
                db.upsert_user_achievement(
                    steam_id,
                    app_id,
                    achievement.get("apiname"),
                    achievement.get("unlocktime")
                )

    db.update_sync(steam_id, int(time.time()))

