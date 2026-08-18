from backend import db
from backend import timeline

def get_player_stats(steam_id):
    games_played = db.get_number_of_games_played(steam_id)[0]
    total_achievements = db.get_number_of_achievements(steam_id)[0]
    games_owned = db.get_user_games(steam_id)
    average_completion_rate = 0
    almost_complete = []
    games_with_achievements = 0 
    user_timeline = timeline.achievements_timeline(steam_id)
    most_active_day = max([(day,len(user_timeline[day])) for day in user_timeline],key = lambda day_num: day_num[1])
    print(most_active_day)
    if not games_owned:
        return None
    for game in games_owned:
        game = game[0]
        number_of_achievements_for_game = db.get_number_of_achievements_for_game(game)[0]

        if number_of_achievements_for_game == 0:
            continue
        games_with_achievements += 1
        number_of_player_achievements_for_game = db.get_number_of_player_achievements_for_game(steam_id,game)[0]
        game_completion_rate = (number_of_player_achievements_for_game)/(number_of_achievements_for_game) 
        if (game_completion_rate > 0.7) and (game_completion_rate < 1):
            almost_complete.append({
                "name": db.get_game_name_from_id(game)[0],
                "unlocked": number_of_player_achievements_for_game,
                "total": number_of_achievements_for_game,
                "percent": round(game_completion_rate * 100)
            })
        average_completion_rate += game_completion_rate 
    average_completion_rate /= games_with_achievements
    print(most_active_day[1])
    return {
        "games_played": games_played,
        "total_achievements": total_achievements,
        "average_completion_rate": round(average_completion_rate * 100),
        "almost_complete": almost_complete,
        "most_active_day": most_active_day[0],
        "stats_unlocked_on_most_active_day" : most_active_day[1]
    }
