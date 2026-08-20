from datetime import datetime
from backend import db


def sort_timeline_by_date(timeline):
    return sorted(timeline, key=lambda achievement: achievement["unlocktime"], reverse=True)


def group_by_date(timeline):
    grouped = {}
    for achievement in timeline:
        date = datetime.fromtimestamp(achievement["unlocktime"]).strftime("%Y-%m-%d")
        if date not in grouped:
            grouped[date] = []
        grouped[date].append(achievement)
    return grouped


def crop(s, max_len=40):
    if s is not None and len(s) > max_len:
        return s[:max_len] + ".."
    return s


def achievements_timeline(user_id):
    rows = db.get_timeline(user_id)

    # Pre-calculate first unlock time per game for "time to unlock"
    first_unlock = {}
    for app_id, _, _, _, _, unlocktime, _ in rows:
        if app_id not in first_unlock or unlocktime < first_unlock[app_id]:
            first_unlock[app_id] = unlocktime

    timeline = []
    for app_id, api_name, game_name, display_name, description, unlocktime, icon in rows:
        date = datetime.fromtimestamp(unlocktime)
        info = {
            "id": api_name,
            "app_id": app_id,
            "api_name": api_name,
            "game_name": crop(game_name, 28),
            "game": crop(game_name, 28),
            "name": crop(display_name, 32),
            "full_name": display_name,
            "full_description": description or "",
            "cropped_description": crop(description, 40),
            "icon": icon,
            "unlocktime": unlocktime,
            "unlock_date": date.strftime("%b %d, %Y"),
            "time_to_unlock": round((unlocktime - first_unlock[app_id]) / 3600, 1),
            "date": {
                "day": date.strftime("%d"),
                "month": date.strftime("%b"),
                "year": date.strftime("%Y"),
                "time": date.strftime("%H:%M")
            }
        }
        timeline.append(info)

    timeline = sort_timeline_by_date(timeline)
    return group_by_date(timeline)