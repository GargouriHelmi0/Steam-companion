from flask import *
from backend.api import steam_api_key
from backend.timeline import achievements_timeline
import requests
import os
from dotenv import load_dotenv
import sqlite3
from backend.db import auto_sync, get_user
from backend.sync import sync_user
from backend.stats import get_player_stats
from backend import api

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]

def valid(steam_id):
    resp = requests.get(f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={steam_api_key}&steamids={steam_id}").json()
    print(resp['response']['players'] != [])
    return (resp['response']['players'] != [])
 
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        steam_id = request.form["steam_id"]
        if valid(steam_id):
            session["steam_id"] = steam_id
            return redirect(url_for("achievements"))
        else:
            return render_template("login.html", error="Invalid steam ID")
    return render_template("login.html")

@app.route("/achievements", methods=["GET", "POST"])
def achievements():
    if "steam_id" not in session:
        return redirect(url_for("home"))

    steam_id = session["steam_id"]
    timeline = achievements_timeline(steam_id)
    stats = get_player_stats(steam_id)

    almost_complete = stats.get("almost_complete", []) if stats else []
    almost_complete.sort(key=lambda g: g["percent"], reverse=True)
    almost_complete = almost_complete[:6]

    perfect_games = stats.get("perfect_games", []) if stats else []
    perfect_games.sort(key=lambda g: g["percent"], reverse=True)
  

    user = get_user(steam_id)
    player_name = user[1] if user else "Player"

    return render_template(
        "achievements.html",
        timeline=timeline,
        stats=stats,
        almost_complete=almost_complete,
        perfect_games=perfect_games,
        player_name=player_name
    )

@app.route("/sync", methods=["POST"])
def sync():
    if "steam_id" not in session:
        return jsonify({"error": "not logged in"}), 401

    sync_user(session["steam_id"])
    return jsonify({"status": "ok"})

@app.route("/api/achievement-stats/<app_id>/<api_name>")
def achievement_stats(app_id, api_name):
    percentages = api.get_global_percentages_for_game_achievements(app_id)
    percent = percentages.get(api_name, 0)

    if percent > 50:
        rarity = "common"
    elif percent > 25:
        rarity = "uncommon"
    elif percent > 10:
        rarity = "rare"
    elif percent > 5:
        rarity = "very rare"
    elif percent > 1:
        rarity = "ultra rare"
    else:
        rarity = "legendary"

    return jsonify({
        "global_rate": round(percent, 1),
        "rarity": rarity
    })

if __name__ == "__main__":
    app.run(debug=True)