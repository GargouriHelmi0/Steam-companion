import db
import api
from datetime import datetime
import time 


def sync_user(steam_id):

    user_info = api.get_user_info(steam_id) 
    steam_name = user_info["response"]["players"][0]["personaname"]
    if db.get_user(steam_id) == None:
        db.add_user(steam_id,steam_name,None)
    owned_games = api.get_owned_games(steam_id)
    for game in owned_games["played_games"] :
            if db.get_game(game[0]) == None:
                db.add_game(game[0],game[1])
            game_info = api.get_game_stats(game[0])

            player_info = api.get_achievements_for_player(steam_id,game[0])
            if game_info is None or player_info is None: 
                continue

            player_stats = player_info.get("playerstats")
            if player_stats is None:
                 continue
            player_achievements = player_stats.get("achievements")
            if player_achievements is None:
                         continue
            game_stats = game_info.get("availableGameStats")
            if game_stats is None:
                         continue
            game_achievements = game_stats.get("achievements")
            if game_achievements is None:
                         continue

            for achievement in game_achievements:
                if db.get_achievement(game[0],achievement.get("name")) is None:
                    db.add_achievement(game[0],achievement.get("name"),achievement.get("displayName"),achievement.get("description"),achievement.get("icon"))

            for achievement in player_achievements :
                if achievement["achieved"] == 1:
                    if db.get_user_achievement(steam_id,game[0],achievement.get("apiname")) is None:
                        db.add_user_achievement(steam_id,game[0],achievement.get("apiname"),achievement.get("unlocktime"))
    db.update_sync(steam_id, int(time.time()))
sync_user(76561198879732674)
