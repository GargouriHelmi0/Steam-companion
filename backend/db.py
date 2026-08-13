import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "steam_companion.db")
conn = sqlite3.connect(db_path)
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
        steam_name TEXT NOT NULL,
        last_sync INTEGER
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
    conn.commit()


def add_user(steam_id,steam_name,last_sync):
    cursor.execute("""
        INSERT INTO users
        VALUES(?,?,?)
        """,(steam_id,steam_name,last_sync))
    conn.commit()

def add_achievement(app_id,achievement_api_name,achievement_display_name,description,icon):
    cursor.execute("""
        INSERT INTO achievements (app_id,achievement_api_name,achievement_display_name,description,icon)
        VALUES (?,?,?,?,?)               
        """,(app_id,achievement_api_name,achievement_display_name,description,icon))
    conn.commit()

def add_user_achievement(steam_id,app_id,achievement_api_name,unlocktime):
    cursor.execute("""
            INSERT INTO user_achievements (steam_id,app_id,achievement_api_name,unlocktime)
            VALUES (?,?,?,?)               
            """,(steam_id,app_id,achievement_api_name,unlocktime))
    conn.commit()


def get_game(app_id):
    cursor.execute("""
        SELECT * FROM games
        WHERE app_id = ?               
        """,(app_id,))
    return cursor.fetchone()
 
def get_user(user_id):
    if user_id == 0:
        cursor.execute("""
                    SELECT * FROM users              
                    """)
        return cursor.fetchall()
    cursor.execute("""
            SELECT * FROM users
            WHERE steam_id = ?               
            """,(user_id,))
    return cursor.fetchone()

def get_achievement(app_id, achievement_api_name):
    cursor.execute("""
        SELECT *
        FROM achievements
        WHERE app_id = ? AND achievement_api_name = ?
    """, (app_id, achievement_api_name))

    return cursor.fetchone()

def get_user_achievement(user_id, app_id, achievement_api_name):
    cursor.execute("""
        SELECT *
        FROM user_achievements
        WHERE steam_id = ?
          AND app_id = ?
          AND achievement_api_name = ?
    """, (user_id, app_id, achievement_api_name))

    return cursor.fetchone()

def get_achievements_for_game(app_id):
    cursor.execute("""
            SELECT * FROM achievements
            WHERE app_id = ?             
            """,(app_id,))
    return cursor.fetchall()

def get_user_achievements_for_game(user_id,app_id):
    cursor.execute("""
            SELECT * FROM user_achievements
            WHERE app_id = ?  AND steam_id = ?             
            """,(app_id,user_id))
    return cursor.fetchall()

def update_sync(user_id,last_sync):
    cursor.execute("""
                UPDATE users
                SET last_sync = ?  WHERE steam_id = ?             
                """,(last_sync,user_id))
    conn.commit()


