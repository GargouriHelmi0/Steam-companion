from flask import *
from backend.api import steam_api_key
from backend.timeline import achievements_timeline
from backend.timeline import achievements_timeline
import requests
import os
from dotenv import load_dotenv
import sqlite3
from backend.db import auto_sync
from backend.sync import sync_user

app = Flask(__name__)
app.secret_key = "123"
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
        else :
            return render_template("login.html",error="Invalid steam ID")
    return render_template("login.html")

@app.route("/achievements", methods=["GET", "POST"])
def achievements():
    if "steam_id" not in session:
        return redirect(url_for("home"))
    steam_id = session["steam_id"]
    timeline =  achievements_timeline(steam_id)
    return render_template("achievements.html",timeline = timeline)

@app.route("/sync", methods=["POST"])
def sync():
    if "steam_id" not in session:
        return jsonify({"error": "not logged in"}), 401

    sync_user(session["steam_id"])
    return jsonify({"status": "ok"})



if __name__ == "__main__":
    app.run(debug=True)