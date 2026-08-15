import api 
from  datetime import datetime
import db

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

    rows = db.get_timeline(user_id)
    timeline = []
    for game, name, description, unlocktime, icon in rows :
        info = dict()
        info["game_name"] = game
        info["achievement_name"] = name
        info["cropped_description"] = crop(description)
        info["icon"] = icon
        info["unlocktime"] = unlocktime
        date = datetime.fromtimestamp(unlocktime)
        info["date"] = {
            "day": date.strftime("%d"),
            "month": date.strftime("%b"),
            "year": date.strftime("%Y"),
            "time": date.strftime("%H:%M")
        }
        timeline.append(info)
    timeline = sort_timeline_by_date(timeline)
    timeline = group_by_date(timeline)
    return timeline



