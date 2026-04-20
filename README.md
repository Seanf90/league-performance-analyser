# League of Legends Performance Analyser

A Python web application that analyses League of Legends player performance using the Riot Games API and compares it with champion statistics scraped from OP.GG.

The project combines **web scraping, database pipelines, and backend analytics** to provide insights into player performance.

---

# University Dissertation Project 

This was created as part of my final year dissertation. The Riot API has since changed, so this code may not run without modifications. Showcasing the architecture and data pipeline design.

---

## Features

* Analyse a player's recent matches
* Calculate performance metrics (KDA, CS/min, etc.)
* Compare player performance with champion averages
* View champion statistics by rank
* Identify best and worst performing players in matches

---

## Tech Stack

* Python
* Flask
* MySQL
* BeautifulSoup
* Pandas
* SQLAlchemy
* Riot Games API

---

## Data Pipeline

This project includes a complete data pipeline:

1. Champion statistics are collected from OP.GG.
2. HTML files are parsed using **BeautifulSoup**.
3. Data is cleaned and structured using **Pandas**.
4. Processed data is written to a **MySQL database**.
5. The **Flask web application** queries this database to analyse player performance.

Pipeline overview:

OP.GG HTML
BeautifulSoup Scraper -> Pandas Data Processing -> MySQL Database -> Flask Analytics Application

---

## Project Structure

```
league-performance-analyser/

app/
    app.py
    services/
        riot_api.py
        match_service.py
        stats_service.py
    database/
        db.py
    utils/
        helpers.py
        performance.py

scraper/
    opgg_scraper.py

data/
    raw/
        champion_stats_gold.html
        champion_stats_plat.html
    sql/
        champion_stats_silver.sql
        champion_stats_plat.sql

requirements.txt
README.md
.gitignore
```

---

## Setup

### 1. Install dependencies

```
pip install -r requirements.txt
```

---

### 2. Configure environment variables

Create a `.env` file in the root of the project:

```
RIOT_API_KEY=your_api_key

DB_USER=root
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_NAME=opggdata
```

---

### 3. Load the database

Import the provided SQL dumps into MySQL:

```
mysql -u root -p opggdata < data/sql/opggdata_champion_stats_silver.sql
```

---

### 4. Run the scraper (optional)

If you want to rebuild the database from raw HTML files:

```
python scraper/opgg_scraper.py
```

---

### 5. Start the web app

```
python app/app.py
```

The application will then be available locally.

---

## Example Use Case

The application analyses a player's recent matches and provides feedback such as:

* CS per minute compared to rank averages
* KDA compared to champion averages
* Performance scoring within the match
* Suggestions for gameplay improvement

---

## Disclaimer

This project uses the Riot Games API but is not endorsed by Riot Games.
