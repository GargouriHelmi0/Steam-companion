# api.py

## `get_game_stats(game_id)`

Fetches the schema (stat definitions & achievements) for a specific game.

**Endpoint:** `ISteamUserStats/GetSchemaForGame/v2`

| Parameter | Type | Description |
|-----------|------|-------------|
| `game_id` | `int` / `str` | Steam App ID (e.g. `730` for CS2, `440` for TF2) |

**Returns:** `dict` — The `"game"` object from the API response.

**Structure:**
```python
{
    "gameName": str,         
    "gameVersion": str,      
    "availableGameStats": {
        "stats": [            
            {
                "name": str,
                "defaultvalue": int,
                "displayName": str
            },
            ...
        ],
        "achievements": [     
            {
                "name": str,
                "defaultvalue": int,
                "displayName": str,
                "hidden": int,       
                "description": str,
                "icon": str,          
                "icongray": str      
            },
            ...
        ]
    }
}
```

**Example:**
```python
stats = get_game_stats(730)
print(stats["gameName"])  
```

---

## `get_user_stats_for_game(user_id, game_id)`

Fetches a specific user's stats & achievements for a specific game.

**Endpoint:** `ISteamUserStats/GetUserStatsForGame/v0002`

| Parameter | Type | Description |
|-----------|------|-------------|
| `user_id` | `str` | 64-bit Steam ID (e.g. `"76561198000000000"`) |
| `game_id` | `int` / `str` | Steam App ID |

**Returns:** `dict` — Raw JSON response from Steam.

**Structure:**
```python
{
    "playerstats": {
        "steamID": str,
        "gameName": str,
        "stats": [             
            {
                "name": str,
                "value": int
            },
            ...
        ],
        "achievements": [      
            {
                "name": str,
                "achieved": int    
            },
            ...
        ]
    }
}
```

> **Note:** If the user has no stats/achievements for the game, the `"stats"` or `"achievements"` keys may be missing entirely.

**Example:**
```python
user_stats = get_user_stats_for_game("76561198000000000", 730)
for ach in user_stats["playerstats"].get("achievements", []):
    print(ach["name"], ach["achieved"])
```

---

## `get_owned_games(user_id)`

Fetches a user's full library with playtime.

**Endpoint:** `IPlayerService/GetOwnedGames/v1`

| Parameter | Type | Description |
|-----------|------|-------------|
| `user_id` | `str` | 64-bit Steam ID |

**Returns:** `dict` — Cleaned summary object.

**Structure:**
```python
{
    "game_count": int,         
    "played_games": [          
        (appid: int, name: str, playtime_forever: int),
        ...
    ]
}
```

- `playtime_forever` is in **minutes**.

**Example:**
```python
library = get_owned_games("76561198000000000")
print(f"Owns {library['game_count']} games")
for appid, name, minutes in library["played_games"]:
    hours = minutes / 60
    print(f"{name}: {hours:.1f}h")
```

---

## `get_achievements_for_player(user_id, game_id)`

Fetches a user's achievement unlock status for a specific game.

**Endpoint:** `ISteamUserStats/GetPlayerAchievements/v0001`

| Parameter | Type | Description |
|-----------|------|-------------|
| `user_id` | `str` | 64-bit Steam ID |
| `game_id` | `int` / `str` | Steam App ID |

**Returns:** `dict` — Raw JSON response from Steam.

**Structure:**
```python
{
    "playerstats": {
        "steamID": str,
        "gameName": str,
        "achievements": [
            {
                "apiname": str,        
                "achieved": int,       
                "unlocktime": int      
            },
            ...
        ],
        "success": bool
    }
}
```

**Example:**
```python
ach = get_achievements_for_player("76561198000000000", 730)
unlocked = [a for a in ach["playerstats"]["achievements"] if a["achieved"]]
print(f"Unlocked {len(unlocked)} achievements")
```

---

## Return Value Cheat Sheet

| Function | Returns | Key Access Pattern |
|----------|---------|-------------------|
| `get_game_stats` | `dict` | `result["gameName"]` / `result["availableGameStats"]["achievements"]` |
| `get_user_stats_for_game` | `dict` | `result["playerstats"]["stats"]` / `result["playerstats"]["achievements"]` |
| `get_owned_games` | `dict` | `result["game_count"]` / `result["played_games"]` (list of tuples) |
| `get_achievements_for_player` | `dict` | `result["playerstats"]["achievements"]` |

---

## Common Steam App IDs

| Game | App ID |
|------|--------|
| Counter-Strike 2 | `730` |
| Dota 2 | `570` |
| Team Fortress 2 | `440` |
| Rust | `252490` |
| PUBG: BATTLEGROUNDS | `578080` |
| Apex Legends | `1172470` |
