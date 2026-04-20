import mysql.connector
from config import DB_CONFIG


def connect_db():
    return mysql.connector.connect(**DB_CONFIG)


def get_average_player_stats(db, summoner_name):

    cursor = db.cursor()

    query = "SELECT * FROM average_player_stats WHERE name = %s"

    cursor.execute(query, (summoner_name,))

    row = cursor.fetchone()

    if not row:
        return None

    columns = cursor.column_names

    return dict(zip(columns, row))