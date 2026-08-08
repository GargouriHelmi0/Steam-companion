# Steam Companion

A Flask web application that connects to a Steam profile and turns a player's achievements into a visual gaming timeline.

The goal is to build a personal Steam dashboard that lets users explore their gaming history, achievements and statistics

## Features

### Currently implemented

* Steam ID input and validation
* Steam Web API integration
* Retrieve owned games
* Retrieve player achievements
* Convert Steam achievement timestamps into readable dates and times
* Group achievements by date
* Display achievements in a timeline
* Display achievement icons, names, games, descriptions, and unlock times
* Interactive achievement selection
* Flask/Jinja frontend


## Tech Stack

* Python
* Flask
* Jinja2
* HTML
* CSS
* JavaScript
* Steam Web API
* Requests
* python-dotenv

## Project Status

**MVP**

The core Steam integration and achievement timeline are working. 
The codebase is still changing frequently, so some features may be incomplete or unstable.

## Known Issues (for available features )

* Achievement retrieval can take a long time especially for profiles with many games.
* Some achievement data may be unavailable depending on the game.
* The frontend is still being refined.
* statistics are not implemented yet.

## Goal for the next version :

- Optimising the game fetching process as it takes a long time 
- Schema caching
- Database data storage
- Error handling
- Input validation enhancements


## Installation

Clone the repository and install the required dependencies:

```bash
git clone <repository-url>
cd <project-folder>
pip install -r requirements.txt
```

Create a `.env` file and add your Steam API key:

```env
STEAM_API_KEY=your_api_key_here
```

Run the Flask application:

```bash
python app.py
```

Then open the local address shown by Flask in your browser.