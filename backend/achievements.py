import requests
import os
from dotenv import load_dotenv
from datetime import datetime
import time
load_dotenv()
steam_api_key = os.getenv("STEAM_API_KEY")

def get_game_stats(game_id):
    stats = requests.get(f"https://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/?appid={game_id}&key={steam_api_key}").json()["game"]
    return stats

def get_player_stats(user_id,game_id):
    return requests.get(f"https://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid={game_id}&key={steam_api_key}&steamid={user_id}").json()

def get_user_stats(user_id):
    res = requests.get(f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={steam_api_key}&steamid={user_id}&include_appinfo=true&include_played_free_games=true").json()
    game_count = res["response"]["game_count"]
    user_stats = dict()
    user_stats["game_count"] = game_count
    user_stats["played_games"] = [(game["appid"],game["name"],game['playtime_forever']) for game in res["response"]["games"]]
    return user_stats
def get_achivements_for_player(user_id , game_id):
    return requests.get(f"https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={game_id}&key={steam_api_key}&steamid={user_id}").json()

def get_owned_games(user_id):# owned games ( ids )
    owned_games = [(info[0],info[1]) for info in get_user_stats(user_id)["played_games"]]
    return owned_games

def sort_timeline_by_date(timeline):
    return sorted(timeline, key=lambda achievement: achievement["unlocktime"],reverse=True)

def group_by_date(timeline):

    grouped = {}
    for achievement in timeline:
        date = datetime.fromtimestamp(achievement["unlocktime"]).strftime("%Y-%m-%d")
        if date not in grouped:
            grouped[date] = []
        grouped[date].append(achievement)
    return grouped

def crop(s):
    if s != None and len(s)>50:
         s = s[:20]+".."
    return s
def achievements_timeline(user_id):
    # returns list of dicts for the timeline ( achievement name , game name , description , date , time , icon )
    #game [0] : game id 
    #game [1] : game name
    timeline = []
    owned_games = get_owned_games(user_id)
    for game in owned_games :
        game_info = get_game_stats(game[0])
        player_info = get_achivements_for_player(user_id,game[0])
        if game_info is None or player_info is None: 
            continue
        game_name = game[1]
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
        schema = {achievement["name"]:achievement for achievement in game_achievements}
        
        for achievement in player_achievements :
            if achievement["achieved"] == 1:
                info = dict()
                info["game"] = game_name
                schema_info = schema.get(achievement["apiname"])
                info["name"] = schema_info.get("displayName")
                info["description"] = schema_info.get("description")
                info["cropped_description"] = crop(schema_info.get("description"))
                info["icon"] = schema_info.get("icon")
                info["unlocktime"] = achievement["unlocktime"]
                date = datetime.fromtimestamp(achievement["unlocktime"])
                info["date"] = {"day": date.strftime("%d"),"month": date.strftime("%b"),"year": date.strftime("%Y"),"time" : date.strftime("%H:%M")}
                timeline.append(info)
    timeline = sort_timeline_by_date(timeline)
    timeline = group_by_date(timeline)
    return timeline