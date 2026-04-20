from flask import Flask, render_template, request

from services.riot_api import fetch_player_info
from services.match_service import fetch_player_matches
from services.stats_service import process_data, calculate_and_return_averages

from database.db import connect_db, get_average_player_stats
from utils.helpers import get_region

from config import RIOT_API_KEY

app = Flask(__name__)

temporary_data = {}


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/stats', methods=['POST'])
def stats():

    summoner_name = request.form['summoner_name']
    server = request.form['server']

    puuid, encrypted_id, player_rank, player_lp = fetch_player_info(
        summoner_name,
        server,
        RIOT_API_KEY
    )

    if not puuid:
        return render_template('error.html')

    region = get_region(server)

    match_data, timeline_data = fetch_player_matches(
        region,
        puuid,
        5,
        RIOT_API_KEY
    )

    db = connect_db()

    stats_data = process_data(
        match_data,
        timeline_data,
        puuid,
        db,
        player_rank
    )

    averages, cs_rec, kda_rec = calculate_and_return_averages(stats_data)

    temporary_data['stats_data'] = stats_data

    return render_template(
        'stats.html',
        summoner_name=summoner_name,
        player_rank=player_rank,
        player_lp=player_lp,
        stats=stats_data,
        averages=averages,
        improvement_cs_recommendation=cs_rec,
        kda_improvement_recommendation=kda_rec
    )


if __name__ == "__main__":
    app.run(debug=True)