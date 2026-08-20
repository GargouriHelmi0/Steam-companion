import sqlite3
import os
from contextlib import contextmanager
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "steam_companion.db")

@contextmanager
def get_db():
    conn = sqlite3.connect(db_path)
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with get_db() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS games (
                app_id INTEGER PRIMARY KEY,
                game_name TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS users (
                steam_id INTEGER PRIMARY KEY,
                steam_name TEXT NOT NULL,
                last_sync INTEGER
            );

            CREATE TABLE IF NOT EXISTS achievements (
                app_id INTEGER,
                achievement_api_name TEXT,
                achievement_display_name TEXT,
                description TEXT,
                icon TEXT,
                PRIMARY KEY (app_id, achievement_api_name),
                FOREIGN KEY (app_id) REFERENCES games(app_id)
            );

            CREATE TABLE IF NOT EXISTS user_achievements (
                steam_id INTEGER,
                app_id INTEGER,
                achievement_api_name TEXT,
                unlocktime INTEGER,
                PRIMARY KEY (steam_id, app_id, achievement_api_name),
                FOREIGN KEY (steam_id) REFERENCES users(steam_id),
                FOREIGN KEY (app_id, achievement_api_name) REFERENCES achievements(app_id, achievement_api_name)
            );

            CREATE TABLE IF NOT EXISTS user_games (
                steam_id INTEGER,
                app_id INTEGER,
                PRIMARY KEY (steam_id, app_id),
                FOREIGN KEY (steam_id) REFERENCES users(steam_id),
                FOREIGN KEY (app_id) REFERENCES achievements(app_id)
            );
        """)
        conn.commit()

init_db()

def upsert_game(app_id, game_name):
    with get_db() as conn:
        conn.execute("""
            INSERT INTO games (app_id, game_name)
            VALUES (?, ?)
            ON CONFLICT (app_id) DO NOTHING
        """, (app_id, game_name))
        conn.commit()


def upsert_user_game(steam_id, app_id):
    with get_db() as conn:
        conn.execute("""
            INSERT INTO user_games (steam_id, app_id)
            VALUES (?, ?)
            ON CONFLICT DO NOTHING
        """, (steam_id, app_id))
        conn.commit()


def upsert_user(steam_id, steam_name, last_sync):
    with get_db() as conn:
        conn.execute("""
            INSERT INTO users (steam_id, steam_name, last_sync)
            VALUES (?, ?, ?)
            ON CONFLICT (steam_id) DO UPDATE SET
                steam_name = excluded.steam_name,
                last_sync = excluded.last_sync
        """, (steam_id, steam_name, last_sync))
        conn.commit()


def upsert_achievement(app_id, achievement_api_name, achievement_display_name, description, icon):
    with get_db() as conn:
        conn.execute("""
            INSERT INTO achievements (app_id, achievement_api_name, achievement_display_name, description, icon)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT (app_id, achievement_api_name) DO NOTHING
        """, (app_id, achievement_api_name, achievement_display_name, description, icon))
        conn.commit()


def upsert_user_achievement(steam_id, app_id, achievement_api_name, unlocktime):
    with get_db() as conn:
        conn.execute("""
            INSERT INTO user_achievements (steam_id, app_id, achievement_api_name, unlocktime)
            VALUES (?, ?, ?, ?)
            ON CONFLICT (steam_id, app_id, achievement_api_name) DO NOTHING
        """, (steam_id, app_id, achievement_api_name, unlocktime))
        conn.commit()


def update_sync(user_id, last_sync):
    with get_db() as conn:
        conn.execute("""
            UPDATE users
            SET last_sync = ?
            WHERE steam_id = ?
        """, (last_sync, user_id))
        conn.commit()


def get_user(user_id):
    with get_db() as conn:
        cursor = conn.cursor()
        if user_id == 0:
            cursor.execute("SELECT * FROM users")
            return cursor.fetchall()
        cursor.execute("SELECT * FROM users WHERE steam_id = ?", (user_id,))
        return cursor.fetchone()


def get_timeline(steam_id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT g.app_id,
                   a.achievement_api_name,
                   g.game_name,
                   a.achievement_display_name,
                   a.description,
                   ua.unlocktime,
                   a.icon
            FROM games g
            JOIN achievements a ON g.app_id = a.app_id
            JOIN user_achievements ua ON g.app_id = ua.app_id
                                      AND a.achievement_api_name = ua.achievement_api_name
            WHERE ua.steam_id = ?
            ORDER BY ua.unlocktime DESC
        """, (steam_id,))
        return cursor.fetchall()

def get_number_of_games_played(steam_id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
                    SELECT count(app_id)
                    FROM user_games
                    WHERE steam_id = ?
            """, (steam_id,))
        return cursor.fetchone()

def get_number_of_achievements(steam_id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
                    SELECT count(app_id)
                    FROM user_achievements
                    WHERE steam_id = ?
                """, (steam_id,))
        return cursor.fetchone()

def get_number_of_achievements_for_game(app_id):
    with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                        SELECT count(app_id)
                        FROM achievements
                        WHERE app_id = ?
                    """, (app_id,))
            return cursor.fetchone()
    
def get_game_name_from_id(app_id):
    with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT game_name FROM games
                WHERE app_id == ?
                """,(app_id,)
            )
            return cursor.fetchone()

def get_number_of_player_achievements_for_game(steam_id,app_id):
     with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                            SELECT count(steam_id)
                            FROM user_achievements
                            WHERE steam_id = ? AND app_id = ?
                        """, (steam_id,app_id))
                return cursor.fetchone()
     
def get_user_games(steam_id):
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                            SELECT app_id
                            FROM user_games
                            WHERE steam_id = ?
                        """, (steam_id,))
                return cursor.fetchall()


def get_most_active_day(steam_id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DATE(unlocktime, 'unixepoch') AS day, COUNT(*) AS cnt
            FROM user_achievements
            WHERE steam_id = ?
            GROUP BY day
            ORDER BY cnt DESC
            LIMIT 1
        """, (steam_id,))
        return cursor.fetchone()

def check_last_sync(steam_id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
                    SELECT last_sync
                    FROM users
                    WHERE steam_id = ?
        """, (steam_id,))
        return cursor.fetchone()

def commit():
    with get_db() as conn:
        conn.commit()

def auto_sync(steam_id):
    if check_last_sync(steam_id)[0] < time.time() - 2*24*60*60 :
        return True
    return False