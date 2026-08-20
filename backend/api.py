import requests
import os
from dotenv import load_dotenv

load_dotenv()
steam_api_key = os.getenv("STEAM_API_KEY")

def get_game_stats(game_id):
    stats = requests.get(f"https://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/?appid={game_id}&key={steam_api_key}&l=en").json()["game"]
    return stats

def get_user_info(user_id):
    return  requests.get(f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={steam_api_key}&steamids={user_id}").json()

def get_user_stats_for_game(user_id,game_id):
    return requests.get(f"https://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid={game_id}&key={steam_api_key}&steamid={user_id}").json()


def get_owned_games(user_id):
    res = requests.get(f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={steam_api_key}&steamid={user_id}&include_appinfo=true&include_played_free_games=true").json()
    game_count = res["response"]["game_count"]
    user_stats = dict()
    user_stats["game_count"] = game_count
    user_stats["played_games"] = [(game["appid"],game["name"],game['playtime_forever']) for game in res["response"]["games"]]
    return user_stats

def get_achievements_for_player(user_id , game_id):
    return requests.get(f"https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={game_id}&key={steam_api_key}&steamid={user_id}").json()

def get_global_percentages_for_game_achievements(app_id):
    global_percentages = requests.get(f"https://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v0002/?gameid={app_id}")
    if global_percentages.status_code == 200:
        global_percentages = global_percentages.json()["achievementpercentages"]["achievements"]
        return {
                achievement["name"]: float(achievement["percent"])
                for achievement in global_percentages
            }
    else :
        return {} 
    

