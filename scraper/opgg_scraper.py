import os
import re
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup
from sqlalchemy import create_engine


RAW_DATA_DIR = Path("data/raw")


def get_html_files():
    """Return all champion stat HTML files."""
    return list(RAW_DATA_DIR.glob("champion_stats_*.html"))


def parse_champion_stats(html_path):
    """Parse champion stats from a saved OP.GG HTML page."""

    with open(html_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file.read(), "html.parser")

    champion_stats = []

    for row in soup.select("table.css-1hfnenn tbody tr"):

        columns = row.select("td")

        if len(columns) < 9:
            continue

        champion_name = columns[1].strong.text

        kda_text = columns[3].span.text
        kda = float(kda_text.split(":")[0])

        win_rate_text = columns[4].text.strip()
        win_rate_match = re.search(r"\d+\.\d+%", win_rate_text)

        win_rate = (
            float(win_rate_match.group().strip("%")) / 100
            if win_rate_match
            else None
        )

        cs = float(columns[7].text.replace(",", ""))
        gold = int(columns[8].text.replace(",", ""))

        champion_stats.append(
            {
                "Champion": champion_name,
                "KDA": kda,
                "Win Rate": win_rate,
                "CS": cs,
                "Gold": gold,
            }
        )

    return champion_stats


def load_to_database(data):

    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST", "localhost")
    db_name = os.getenv("DB_NAME", "opggdata")

    engine = create_engine(
        f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"
    )

    for table_name, rows in data.items():

        df = pd.DataFrame(rows)

        df.to_sql(
            table_name,
            engine,
            index=False,
            if_exists="replace",
        )


def scrape_opgg():

    html_files = get_html_files()

    if not html_files:
        print("No HTML files found in data/raw/")
        return

    all_champion_stats = {}

    for file_path in html_files:

        print(f"Processing {file_path.name}")

        stats = parse_champion_stats(file_path)

        table_name = file_path.stem

        all_champion_stats[table_name] = stats

    load_to_database(all_champion_stats)

    print("Champion stats successfully written to database.")


if __name__ == "__main__":
    scrape_opgg()