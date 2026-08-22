# Steam Companion

A Flask web application that connects to a Steam profile and turns a player's achievements into a visual gaming timeline.

The goal is to build a personal Steam dashboard where users can explore their gaming history, achievements, and statistics.

## Features

### Currently implemented

* Steam ID input and validation
* Steam Web API integration
* Retrieve owned games
* Retrieve player achievements
* Retrieve game achievement schemas
* Retrieve Steam profile information
* SQLite database for persistent data storage
* Store users, games, achievements, and user achievements
* Database relationships and foreign keys
* Incremental database insertion using `ON CONFLICT`
* Track the user's last synchronization time
* Convert Steam achievement timestamps into readable dates and times
* Group achievements by date
* Display achievements in a timeline
* Display achievement icons, names, games, descriptions, and unlock times
* Interactive achievement selection
* Flask/Jinja frontend

## Tech Stack

- Python, Flask, Jinja2
- SQLite
- Steam Web API, Requests
- HTML, CSS, JavaScript

## Project Status

**MVP**

The core Steam integration, database system, synchronization system, and achievement timeline are working.

The project is still under active development, with statistics and performance improvements planned for future versions.

## Known Issues

* Initial synchronization can take a long time for profiles with many games.
* Steam API requests can be slow or unavailable for some games.
* Synchronization currently still makes many API requests even when most data is already stored locally.

## Future Goals

### Synchronization

* Incremental synchronization
* Only fetch data that has changed since the previous sync
* Improve schema caching
* Reduce unnecessary Steam API requests
* Improve error handling
* Allow synchronization to happen without making the user wait for the data
* Improve handling of failed or unavailable Steam API requests

### Performance

* Improve caching
* Improve synchronization speed

### Functionality

* Add more statistics 


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