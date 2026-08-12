import sqlite3

conn = sqlite3.connect("steam_companion.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS games (
        app_id INTEGER PRIMARY KEY,
        game_name TEXT NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        steam_id INTEGER PRIMARY KEY,
        steam_name TEXT NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS achievements (
        app_id INTEGER,
        achievement_api_name TEXT,
        achievement_display_name TEXT NOT NULL,
        description TEXT,
        icon TEXT,
        PRIMARY KEY (app_id, achievement_api_name),
        FOREIGN KEY (app_id) REFERENCES games(app_id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_achievements (
        steam_id INTEGER,
        app_id INTEGER,
        achievement_api_name TEXT,
        unlocktime INTEGER,
        PRIMARY KEY (steam_id, app_id, achievement_api_name),
        FOREIGN KEY (steam_id) REFERENCES users(steam_id),
        FOREIGN KEY (app_id, achievement_api_name)
            REFERENCES achievements(app_id, achievement_api_name)
    )
""")

def add_game(app_id,game_name):
    cursor.execute("""
    INSERT INTO games (app_id,game_name)
    VALUES(?,?)
    """,(app_id,game_name))
def add_user(steam_id,steam_name):
    cursor.execute("""
        INSERT INTO users
        VALUES(?,?)
        """,(steam_id,steam_name))

def get_game(app_id):
    cursor.execute("""
        SELECT * FROM games
        WHERE app_id = ?               
        """,(app_id,))
    return cursor.fetchone()

def add_achievement(app_id,achievement_api_name,achievement_display_name,description,icon):
    cursor.execute("""
        INSERT INTO achievements (app_id,achievement_api_name,achievement_display_name,description,icon)
        VALUES (?,?,?,?,?)               
        """,(app_id,achievement_api_name,achievement_display_name,description,icon))


def add_user_achievement(steam_id,app_id,achievement_api_name,unlocktime):
    cursor.execute("""
            INSERT INTO user_achievements (steam_id,app_id,achievement_api_name,unlocktime)
            VALUES (?,?,?,?)               
            """,(steam_id,app_id,achievement_api_name,unlocktime))


conn.commit()
