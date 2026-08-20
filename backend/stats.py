from backend import db

def get_player_stats(steam_id):
    """
    to add:
    - stats heatmap
    -longest streak
    -current streak
    -best achievements
    
    """
    games_played = db.get_number_of_games_played(steam_id)[0]
    total_achievements = db.get_number_of_achievements(steam_id)[0]
    games_owned = db.get_user_games(steam_id)

    if not games_owned:
        return None

    average_completion_rate = 0
    almost_complete = []
    perfect_games = []
    games_with_achievements = 0

    for game_row in games_owned:
        game = game_row[0]
        number_of_achievements_for_game = db.get_number_of_achievements_for_game(game)[0]

        if number_of_achievements_for_game == 0:
            continue

        games_with_achievements += 1
        number_of_player_achievements_for_game = db.get_number_of_player_achievements_for_game(steam_id, game)[0]
        game_completion_rate = number_of_player_achievements_for_game / number_of_achievements_for_game

        game_info = {
            "name": db.get_game_name_from_id(game)[0],
            "unlocked": number_of_player_achievements_for_game,
            "total": number_of_achievements_for_game,
            "percent": round(game_completion_rate * 100)
        }

        if game_completion_rate == 1.0:
            perfect_games.append(game_info)
        elif game_completion_rate > 0.7:
            almost_complete.append(game_info)

        average_completion_rate += game_completion_rate

    average_completion_rate /= games_with_achievements

    most_active = db.get_most_active_day(steam_id)
    if most_active:
        most_active_day = most_active[0]
        stats_unlocked_on_most_active_day = most_active[1]
    else:
        most_active_day = "N/A"
        stats_unlocked_on_most_active_day = 0

    return {
        "games_played": games_played,
        "total_achievements": total_achievements,
        "average_completion_rate": round(average_completion_rate * 100),
        "almost_complete": almost_complete,
        "perfect_games": perfect_games,
        "most_active_day": most_active_day,
        "stats_unlocked_on_most_active_day": stats_unlocked_on_most_active_day
    }